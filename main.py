# main.py
"""
Quantum HTTP wrapper

Exposes a single POST /generate_deck endpoint that:
- Accepts a title and financial_data payload
- Calls turbo_create_presentation() to generate a .pptx
- Returns the finished PowerPoint file as the response
"""

import os
import uuid
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from quantum_turbo import turbo_create_presentation


# Path to your master/reference deck.
# Put QUANTUN.HUZZAHH.pptx in the repo root, or override via env var.
MASTER_DECK_PATH: str = os.getenv(
    "QUANTUM_MASTER_DECK_PATH",
    "QUANTUN.HUZZAHH.pptx"
)


class DeckRequest(BaseModel):
    """
    Minimal request schema.

    financial_data should follow the structure expected by
    turbo_create_presentation / Quantum:
      {
        "metrics": {...},
        "table": [...],
        "comparisons": {...},
        "analysis": {"trend": "positive" | "neutral" | "negative"},
        ...
      }
    """
    title: str
    financial_data: Dict[str, Any]
    # Optional override of reference deck if you ever need it
    reference_deck_path: Optional[str] = None


app = FastAPI(title="Quantum Deck Generator")


@app.post("/generate_deck")
def generate_deck(payload: DeckRequest):
    """
    Generate a Quantum PowerPoint deck and return it as a file download.
    """
    # Determine which reference deck to use
    reference_path = payload.reference_deck_path or MASTER_DECK_PATH

    if not os.path.exists(reference_path):
        # Fail fast if the reference deck is missing
        raise HTTPException(
            status_code=500,
            detail=f"Reference deck not found at {reference_path}"
        )

    # Build a unique filename in /tmp for Render
    output_filename = f"quantum_{uuid.uuid4()}.pptx"
    output_path = os.path.join("/tmp", output_filename)

    try:
        # Call the high-speed Quantum generator
        generated_path, _generation_time = turbo_create_presentation(
            title=payload.title,
            financial_data=payload.financial_data,
            reference_deck_path=reference_path,
            output_filename=output_path,
            verbose=False,
        )

        if not os.path.exists(generated_path):
            raise RuntimeError(
                f"Deck generator did not produce file at {generated_path}"
            )

        # Return the PPTX as the HTTP response
        return FileResponse(
            generated_path,
            media_type=(
                "application/"
                "vnd.openxmlformats-officedocument.presentationml.presentation"
            ),
            filename="Quantum_Deck.pptx",
        )

    except HTTPException:
        # Re-raise explicit HTTP errors
        raise

    except Exception as exc:
        # Generic failure path
        raise HTTPException(
            status_code=500,
            detail=f"Deck generation failed: {exc}"
        )
