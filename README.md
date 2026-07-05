<p align="center">
  <img src="SenseSight/app/frontend/static/images/logo.png" alt="SenseSight logo" width="160">
</p>

<h1 align="center">SenseSight</h1>

<p align="center"><em>Turning sights into sounds — AI-powered object detection with spatial audio feedback to help visually impaired people navigate the world around them.</em></p>

<p align="center">
  🎬 <a href="SenseSight_object_detection/introducing_SenseSight.mp4"><strong>Watch the introduction video</strong></a>
</p>

---

SenseSight is an accessibility platform that uses real-time computer vision to detect objects in a person's surroundings and describe them through spoken, position-aware audio cues ("person on slight left", "car on right"). It pairs a YOLO-based detection engine with a user-facing web dashboard that manages accounts and visualizes detection history.

> **Project Focus**
>
> The **Detection Engine** is the core of SenseSight. It is designed to be integrated into wearable hardware (e.g., smart glasses with a camera) to provide real-time object detection and spatial audio guidance for visually impaired users. The **Web Platform** is a supporting tool for analytics and research, enabling hospitals and researchers to monitor detection history and evaluate system usage over time.

This repository is a monorepo containing two independent FastAPI services:

| Service | Folder | Port | Responsibility |
|---------|--------|------|----------------|
| **Web Platform** | [`SenseSight/`](SenseSight/) | `8000` | User authentication, dashboard, profile management, detection history & analytics |
| **Detection Engine** | [`SenseSight_object_detection/`](SenseSight_object_detection/) | `8080` | Real-time/uploaded video object detection, multi-object tracking, spatial text-to-speech feedback, annotated video output |

Each service has its own detailed Instruction file:
- 📘 [Web Platform](SenseSight/README.md)
- 📙 [Detection Engine](SenseSight_object_detection/README.md)

---

## Architecture Overview

```
                        ┌──────────────────────────────────────┐
                        │             End User                 │
                        │   (visually impaired person / admin) │
                        └───────────────┬──────────────────────┘
                                        │
                 ┌──────────────────────┴───────────────────────┐
                 │                                              │
                 ▼                                              ▼
   ┌──────────────────────────────┐            ┌─────────────────────────────────┐
   │   SenseSight Web Platform    │            │   SenseSight Detection Engine   │
   │   (FastAPI · port 8000)      │            │   (FastAPI · port 8080)         │
   │                              │            │                                 │
   │  • JWT auth (cookies)        │            │  • YOLOv11 (yolo11s.pt)         │
   │  • Jinja2 dashboard          │            │  • BoT-SORT multi-object track  │
   │  • Detection history charts  │            │  • Spatial audio (pyttsx3 TTS)  │
   │  • MySQL persistence         │            │  • Annotated WebM video output  │
   │                              │            │  • MJPEG live/upload streaming  │
   │  MVC: controller→service→    │            │  MVC: controller→service        │
   │       dao→vo + schemas       │            │                                 │
   └──────────────────────────────┘            └─────────────────────────────────┘
              │                                               
              ▼                                               
        ┌────────────┐                                         
        │    MySQL   │                                         
        │ sensesight │                                         
        └────────────┘                                         
```

> **Note:** The two services currently run independently. The detection engine performs detection and returns object counts; the web platform exposes a `POST /dashboard/store_detection` endpoint designed to persist those counts so they can be aggregated and charted on the user's history page.

---

## Technology Stack

**Shared foundation**
- **Python** 3.x
- **FastAPI** 0.115.6 + **Uvicorn** ASGI server
- **PyTorch** 2.5.1 / **TorchVision** 0.20.1 — deep-learning backend
- **Ultralytics YOLO** — object detection
- **OpenCV** — image/video processing
- **Jinja2** — server-side HTML templating

**Web Platform specifics**
- **SQLAlchemy** 1.4 + **MySQL** (PyMySQL driver)
- **PyJWT** + **passlib/bcrypt** — token auth & password hashing
- **Chart.js** — history visualization

**Detection Engine specifics**
- **pyttsx3** — text-to-speech for spatial audio feedback
- **FFmpeg / python-ffmpeg** — audio/video muxing into WebM
- **BoT-SORT** — multi-object tracking

---

## Getting Started

### Prerequisites
- Python 3.10+ and `pip`
- MySQL 8.x running locally (for the Web Platform)
- FFmpeg installed and available on `PATH` (for the Detection Engine)
- A webcam (optional — for live detection)

### Clone

```bash
git clone <repository-url>
cd SenseSight
```

### Run the services

Each service is set up and launched independently. Follow the per-service guides:

1. **Web Platform** → [`Set-up Instructions`](SenseSight/README.md) (runs on http://127.0.0.1:8000)
2. **Detection Engine** → [`Set-up Instructions`](SenseSight_object_detection/README.md) (runs on http://localhost:8080)

We recommend a **separate virtual environment per service**, since they pin slightly different dependency versions.

---

## Repository Layout

```
SenseSight/
├── README.md                       ← you are here (monorepo overview)
├── .gitignore
│
├── SenseSight/                     ← Web Platform (auth, dashboard, history)
│   ├── app/
│   │   ├── main.py
│   │   ├── config/                 (database, security/JWT)
│   │   ├── controllers/            (auth, dashboard, detection data)
│   │   ├── services/               (business logic)
│   │   ├── dao/                    (database access)
│   │   ├── vo/                     (SQLAlchemy models)
│   │   ├── schemas/                (Pydantic models)
│   │   ├── utils/                  (auth utils, logger)
│   │   └── frontend/               (Jinja2 templates + static assets)
│   ├── requirements.txt
│   └── README.md
│
└── SenseSight_object_detection/    ← Detection Engine (YOLO + TTS)
    ├── app/
    │   ├── main.py
    │   ├── controller/             (detection endpoints)
    │   ├── services/               (YOLO detection + tracking + TTS)
    │   ├── templates/              (single-page UI)
    │   └── static/                 (JS + CSS)
    ├── yolo11s.pt                  (YOLOv11-small pretrained weights)
    ├── requirements.txt
    └── README.md
```

---

## Key Features

-  **Real-time object detection** on webcam and uploaded video using YOLOv11
-  **Spatial audio feedback** — detected objects are announced with their position (left / center / right)
-  **Multi-object tracking** with BoT-SORT for accurate, de-duplicated object counts
-  **Annotated video export** — output video with bounding boxes, IDs, counts, and synthesized audio (WebM)
-  **User accounts** with secure JWT authentication and bcrypt-hashed passwords
-  **Detection history & analytics** — aggregated object counts visualized as charts
-  **Clean layered (MVC) architecture** in both services

---

## Future Enhancements

SenseSight is an active project, and future work includes:

-  Deploying the Detection Engine on wearable smart glasses for real-world use.
-  Optimizing inference for edge devices such as Raspberry Pi and NVIDIA Jetson.
-  Adding distance estimation and obstacle-aware navigation.
-  Integrating GPS and voice commands for smarter outdoor assistance.
-  Expanding the Web Platform with richer analytics for hospitals and accessibility research.

---

## License

This project is provided for educational and accessibility-research purposes. See the [LICENSE](LICENSE) file for details.
