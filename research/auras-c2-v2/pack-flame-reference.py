"""Pack unchanged C2 flames; return atlas and LEFT-half (x,y,hs,data) chunks.

Coordinates use the original 64x112 bitmap. Mirror the returned chunks to draw
the right half. Atlas data is native 4bpp; each tile occupies 32 bytes.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pack_c2 as source

TILE_BYTES = 32


def _trim(chunk):
    x, y, hs, data = chunk
    while data and not any(data[:32]):
        y += 8
        data = data[32:]
    while data and not any(data[-32:]):
        data = data[:-32]
    return (x, y, len(data) // 4, data) if data else None


def _atlas(chunks):
    return source.merge_tiles([c[3] for c in chunks])


def _key(chunks):
    return tuple((c[0], c[1], c[2]) for c in chunks)


def _split_options(chunks):
    for i, (x, y, hs, data) in enumerate(chunks):
        for at in range(8, hs, 8):
            split = [_trim((x, y, at, data[:at * 4])),
                     _trim((x, y + at, hs - at, data[at * 4:]))]
            yield tuple(sorted(chunks[:i] + tuple(c for c in split if c) + chunks[i+1:]))


def pack_flame(width=64, height=112, max_tiles=40, max_sprites=38):
    """Return (atlas_bytes, chunks), preserving every indexed bitmap pixel.

    Trims only blank end tiles and searches a bounded beam of vertical splits.
    max_sprites includes BOTH mirrored halves, so at most 19 chunks by default.
    """
    pixels = source.load(width, height)
    initial = tuple(c for c in (_trim(c) for c in source.chunks(pixels, width, height)) if c)
    limit = max_sprites // 2
    beam = [initial]
    visited = {_key(initial)}
    best = None
    for count in range(len(initial), limit + 1):
        scored = [(len(atlas := _atlas(cs)) // 32, len(cs), _key(cs), atlas, cs) for cs in beam]
        scored.sort(key=lambda v: v[:3])
        if scored and (best is None or scored[0][:3] < best[:3]):
            best = scored[0]
        valid = [v for v in scored if v[0] <= max_tiles]
        if valid:
            # This is the first successful split count: minimum sprite count
            # within this search, then smallest atlas among the retained beam.
            chosen = valid[0]
            verify_identity(pixels, width, height, chosen[3], chosen[4])
            return chosen[3], list(chosen[4])
        if count == limit:
            break
        next_beam = []
        for _, _, _, _, cs in scored[:96]:
            for candidate in _split_options(cs):
                key = _key(candidate)
                if len(candidate) <= limit and key not in visited:
                    visited.add(key)
                    next_beam.append(candidate)
        beam = next_beam
    raise ValueError(f'Cannot reach {max_tiles} tiles / {max_sprites} sprites; best={best[:2]}')


def verify_identity(pixels, width, height, atlas, chunks):
    """Draw atlas-backed chunks and their mirrors, checking complete identity."""
    rendered = [0] * (width * height)
    for x, y, hs, data in chunks:
        starts = [at for at in range(0, len(atlas) - len(data) + 1, 32) if atlas[at:at+len(data)] == data]
        assert starts, 'Chunk missing from tile-aligned atlas'
        at = starts[0]
        assert hs in (8, 16, 24, 32)
        for dy in range(hs):
            for dx in range(8):
                byte = atlas[at + (dy // 8) * 32 + (dy % 8) * 4 + dx // 2]
                color = (byte >> (0 if dx & 1 else 4)) & 15
                rendered[(y + dy) * width + x + dx] = color
                rendered[(y + dy) * width + width - x - dx - 1] = color
    assert rendered == pixels, f'Pixel mismatch: {sum(a != b for a,b in zip(rendered,pixels))}'


if __name__ == '__main__':
    atlas, chunks = pack_flame()
    print(f'Flames: {len(atlas)//32} tiles; {len(chunks)} left chunks; {len(chunks)*2} sprites mirrored')
    print('Pixel identity: PASS')
    print('Chunks:', [(x,y,hs) for x,y,hs,_ in chunks])
