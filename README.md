# AIDP RenderHub — Blender GPU Render Worker

A GPU-powered Blender render worker packaged as a Docker image.  
Built for the **AIDP.store GPU Campaign** (Superteam Earn bounty).

This project enables running Blender rendering workloads on decentralized GPU compute providers such as AIDP.

---

## What this does

- Takes a Blender `.blend` file
- Renders frames using Blender CLI (Cycles)
- Outputs:
  - PNG frames, OR
  - MP4 video (via ffmpeg)
- Designed to run as a **GPU compute worker** (Docker container)

---

## Docker Image

Pull worker image:

```bash
docker pull majesticl/aidp-render-worker:latest
