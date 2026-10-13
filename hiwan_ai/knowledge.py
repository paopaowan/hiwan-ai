"""Phase 2: read-only Markdown passage discovery and lexical candidate retrieval.

This layer ranks relevance, not authoritativeness. Authority is resolved separately.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

EXCLUDED_DIRS = frozenset({
    '.git', '.venv', '.hiwan', 'node_modules', '__pycache__',
    'private', 'memory', 'secrets', 'credentials',
})
STOPWORDS = frozenset({
    'a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do',
    'does', 'for', 'from', 'how', 'in', 'is', 'it', 'of', 'on',
    'or', 'our', 'the', 'this', 'to', 'was', 'what', 'when', 'where',
    'which', 'who', 'why', 'with', 'hiwan', 'ai',
})
WORD_RE = re.compile(r'[^\W_]+', re.UNICODE)
SECTION_RE = re.compile(r'^(#{2,4})\s+(.+?)\s*$', re.MULTILINE)
HEADING_RE = re.compile(r'^(#{1,4})[ \t]+(.+?)[ \t]*$')
FENCE_RE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
MAX_PASSAGE_LINES = 90
WINDOW_LINES = 65
OVERLAP_LINES = 12


def _markdown_headings(lines: list[str]) -> dict[int, tuple[int, str]]:
    """ATX headings outside fenced code (backtick or tilde fences)."""
    headings: dict[int, tuple[int, str]] = {}
    fence_char = ''
    fence_width = 0
    for i, line in enumerate(lines):
        marker = FENCE_RE.match(line)
        if fence_char:
            if (marker and marker.group(1)[0] == fence_char
                    and len(marker.group(1)) >= fence_width
                    and not marker.group(2).strip()):
                fence_char = ''
                fence_width = 0
            continue
        if marker:
            fence_char = marker.group(1)[0]
            fence_width = len(marker.group(1))
            continue
        match = HEADING_RE.match(line)
        if match:
            headings[i] = (len(match.group(1)), match.group(2).strip())
    return headings


def tokenize(text: str) -> tuple[str, ...]:
    return tuple(WORD_RE.findall(text.casefold()))


def query_terms(query: str) -> tuple[str, ...]:
    raw = tuple(dict.fromkeys(tokenize(query)))
    useful = tuple(t for t in raw if t not in STOPWORDS)
    return useful or raw


@dataclass(frozen=True)
class KnowledgeDocument:
    path: str
    title: str
    content: str


@dataclass(frozen=True)
class SearchHit:
    path: str
    title: str
    snippet: str
    score: int
    matched_terms: int
    total_terms: int
    heading: str = ''
    start_line: int = 1
    end_line: int = 1

    @property
    def reference(self) -> str:
        return f'{self.path}:L{self.start_line}-L{self.end_line}'


@dataclass(frozen=True)
class _Passage:
    path: str
    title: str
    heading: str
    start_line: int
    end_line: int
    content: str


class MarkdownKnowledgeBase:
    def __init__(self, root: Path | str, *, excluded_dirs: set[str] | None = None):
        self.root = Path(root).expanduser().resolve()
        self.excluded_dirs = frozenset(
            part.casefold() for part in EXCLUDED_DIRS | frozenset(excluded_dirs or ())
        )
        if not self.root.exists():
            raise FileNotFoundError(self.root)
        if not self.root.is_dir():
            raise NotADirectoryError(self.root)

    def _safe_markdown_files(self):
        for path in sorted(self.root.rglob('*.md')):
            relative = path.relative_to(self.root)
            if any(part.casefold() in self.excluded_dirs for part in relative.parts[:-1]):
                continue
            if path.is_symlink() or not path.is_file():
                continue
            # Hard links may alias private files outside the checkout.
            try:
                if path.stat().st_nlink > 1:
                    continue
            except OSError:
                continue
            # Protect even against links through intermediate directories.
            if not path.resolve().is_relative_to(self.root):
                continue
            yield path

    def discover(self) -> list[KnowledgeDocument]:
        result = []
        for path in self._safe_markdown_files():
            text = path.read_text(encoding='utf-8', errors='replace')
            headings = _markdown_headings(text.splitlines())
            title = next((name for level, name in headings.values()
                          if level == 1), path.stem)
            result.append(KnowledgeDocument(
                path=path.relative_to(self.root).as_posix(),
                title=title,
                content=text,
            ))
        return result

    @staticmethod
    def _passages(doc: KnowledgeDocument) -> list[_Passage]:
        """Split by Markdown sections, subdividing only *oversized* sections.

        Small accepted decisions retain their rationale within the same
        passage. Long learning logs and heading-free imported reviews are
        split into line-bounded, overlapping evidence windows.
        """
        lines = doc.content.splitlines()
        if not lines:
            return []

        headings = _markdown_headings(lines)
        main_headings = [index for index, (level, _) in headings.items()
                         if level == 2]
        main_starts = ([0] if not main_headings or main_headings[0] != 0 else [])
        main_starts += main_headings
        main_ends = main_starts[1:] + [len(lines)]
        result: list[_Passage] = []

        def emit(begin: int, finish: int, heading: str) -> None:
            if finish <= begin:
                return
            if finish - begin <= MAX_PASSAGE_LINES:
                text = '\n'.join(lines[begin:finish]).strip()
                if text:
                    result.append(_Passage(
                        doc.path, doc.title, heading,
                        begin + 1, finish, text,
                    ))
                return
            offset = 0
            length = finish - begin
            while offset < length:
                win_start = begin + offset
                win_end = min(finish, win_start + WINDOW_LINES)
                text = '\n'.join(lines[win_start:win_end]).strip()
                if text:
                    result.append(_Passage(
                        doc.path, doc.title, heading,
                        win_start + 1, win_end, text,
                    ))
                if win_end == finish:
                    break
                offset += WINDOW_LINES - OVERLAP_LINES

        for start, end in zip(main_starts, main_ends):
            info = headings.get(start)
            heading = info[1] if info and info[0] == 2 else doc.title
            subheadings = [
                (i, level, name)
                for i, (level, name) in headings.items()
                if start < i < end and level > 2
            ]
            if end - start <= MAX_PASSAGE_LINES:
                # Keep concise decisions together, but preserve subheading terms.
                names = [name for _, _, name in subheadings]
                emit(start, end, ' / '.join([heading] + names))
                continue
            sub_starts = ([start] if not subheadings else [start] + [i for i, _, _ in subheadings])
            sub_ends = sub_starts[1:] + [end]
            by_start = {i: (level, name) for i, level, name in subheadings}
            ancestors: list[tuple[int, str]] = []

            for begin, finish in zip(sub_starts, sub_ends):
                info = by_start.get(begin)
                if info:
                    level, name = info
                    ancestors = [(l, n) for l, n in ancestors if l < level]
                    ancestors.append((level, name))
                subheading = ' / '.join([heading] + [n for _, n in ancestors])
                emit(begin, finish, subheading)

        return result

    @classmethod
    def _focused_snippet(cls, content: str,
                         terms: tuple[str, ...], max_chars: int = 2000) -> str:
        if len(content) <= max_chars:
            return content

        # Choose a locally relevant excerpt instead of unconditionally taking
        # the first 1000 characters of a long Markdown passage.
        matches = list(WORD_RE.finditer(content.casefold()))
        positions = [m.start() for m in matches if m.group() in terms]
        if not positions:
            return content[:max_chars].rstrip() + '\n...'

        best_start, best_score = 0, -1
        for pos in positions:
            start = max(0, min(pos - max_chars // 3, len(content) - max_chars))
            window = content[start:start + max_chars]
            words = tokenize(window)
            coverage = len(set(words) & set(terms))
            phrase = cls._longest_query_phrase(words, terms)
            score = 10 * coverage + 5 * phrase * phrase
            if score > best_score:
                best_start, best_score = start, score
        snippet = content[best_start:best_start + max_chars].strip()
        return ('...\n' if best_start else '') + snippet + ('\n...' if best_start + max_chars < len(content) else '')

    @staticmethod
    def _longest_query_phrase(words: tuple[str, ...], terms: tuple[str, ...]) -> int:
        # Count the longest consecutive run of query terms present in the
        # passage. Unlike frequency scores, this cannot grow with repetitions.
        if not words or not terms:
            return 0
        for size in range(len(terms), 1, -1):
            for index in range(len(terms) - size + 1):
                target = terms[index:index + size]
                if any(words[offset:offset + size] == target
                       for offset in range(len(words) - size + 1)):
                    return size
        return 0

    @classmethod
    def _rank(cls, passage: _Passage, terms: tuple[str, ...]) -> SearchHit | None:
        heading_words = tokenize(passage.heading)
        body_words = tokenize(passage.content)
        heading_set = set(heading_words)
        body_set = set(body_words)
        matched = sum(term in body_set or term in heading_set for term in terms)
        if not matched:
            return None
        heading_matches = sum(term in heading_set for term in terms)
        phrase_size = cls._longest_query_phrase(body_words, terms)
        # Coverage, heading alignment, and contiguous phrase. No raw term
        # frequency: repeating the same phrase 100 times cannot game rank.
        score = (12 * matched + 7 * heading_matches +
                 5 * phrase_size * phrase_size)
        # Keep text source-exact and focus large excerpts near query terms.
        snippet = cls._focused_snippet(passage.content, terms)
        return SearchHit(
            path=passage.path, title=passage.title,
            heading=passage.heading, snippet=snippet, score=score,
            matched_terms=matched, total_terms=len(terms),
            start_line=passage.start_line, end_line=passage.end_line,
        )

    def search(self, query: str, *, limit: int = 16) -> list[SearchHit]:
        if not query.strip():
            raise ValueError('query must not be empty')
        if limit < 1:
            raise ValueError('limit must be >= 1')
        terms = query_terms(query)
        if not terms:
            raise ValueError('query must contain searchable terms')
        hits = []
        for document in self.discover():
            for passage in self._passages(document):
                hit = self._rank(passage, terms)
                if hit is not None:
                    hits.append(hit)
        hits.sort(key=lambda hit: (-hit.score, -hit.matched_terms,
                                   hit.path, hit.start_line))
        return hits[:limit]
