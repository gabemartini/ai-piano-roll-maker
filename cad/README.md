# CAD

Mechanical design for the piano roll cutter, written in [build123d](https://github.com/gumyr/build123d)
(Python, OpenCascade kernel). Each part is a script in `parts/`; shared dimensions live in `params.py`.

## Layout

| Path | What it holds |
| --- | --- |
| `params.py` | Roll formats (88-note and 65-note), bearings on hand, FDM tolerances |
| `parts/` | One script per part; running it writes STEP + STL to `exports/` |
| `exports/` | Generated STEP (CAM, other CAD) and STL (slicer) files |

## Switching roll format

Set `ROLL = ROLL_88` or `ROLL = ROLL_65` in `params.py`, then re-run the part scripts.
The edge offsets are derived by centring the tracks on 11 1/4 in paper, so measure a real roll
before relying on them. 65-note spool drive-pin dimensions are still to be measured.

## Working with Claude

The repo's `.mcp.json` registers the [build123d-mcp](https://github.com/pzfreo/build123d-mcp)
server, so Claude Code (local, Remote Control or cloud) can build, render, measure and check
interference between parts. It needs [uv](https://docs.astral.sh/uv/) on the PATH.
Code run through the MCP server lives only in that session, so ask Claude to save the final
version to the part's script here.

## Running a part by hand

```sh
pip install build123d
python cad/parts/bearing_test_fit.py
```

## First print: bearing test fit

`parts/bearing_test_fit.py` makes one coupon per bearing (608 skateboard, MR106ZZ) with seats from
-0.2 to +0.2 mm around the nominal OD. Press a bearing into each seat, pick the one that grips
without cracking, and put that offset in `PRESS_FIT` in `params.py`.
