# Build Log - Day 2: Docker Deepening

---

## 1. What part of the Dockerfile installs dependencies?

The dependencies are installed using the following line in the Dockerfile:

```bash
RUN pip install --no-cache-dir -r requirements.txt

--- 

## 2. Why do we use 0.0.0.0 instead of 127.0.0.1?

We use 0.0.0.0 because it makes the application accessible from outside the container (such as the browser on the host machine).

127.0.0.1 → only accessible inside the container (localhost of container)
0.0.0.0 → exposes the service to the host machine and external access

Without 0.0.0.0, the FastAPI app would not be reachable from the browser.

---

## 3. What happened when you removed a dependency?

When a dependency like fastapi was removed from requirements.txt:

Docker did not install that package inside the container
The application failed with ModuleNotFoundError
This proves that Docker strictly follows requirements.txt and does not assume missing dependencies

---

##4. Why is deleting your venv powerful psychologically?

Deleting the local venv shows that:

The local Python environment is not required anymore
The application runs completely inside Docker
The system becomes portable and independent of your machine

This creates confidence that the project will run the same way on any system.