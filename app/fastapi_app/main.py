"""Minimal FastAPI entrypoint for local development and testing.

This file provides a small, safe FastAPI app that can be imported and run
by tests or developers. It intentionally keeps dependencies minimal.
"""
from fastapi import FastAPI

app = FastAPI(title="CultivAR - Minimal FastAPI")


@app.get("/")
def read_root():
    return {"message": "CultivAR FastAPI app (minimal)"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
