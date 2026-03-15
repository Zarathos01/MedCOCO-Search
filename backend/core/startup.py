import logging

logger = logging.getLogger(__name__)


def load_models():
    """
    Load MedCLIP and MedBLIP models into memory.
    Called once on server startup — this may take 1-2 minutes on first run
    as it downloads model weights from HuggingFace.
    """
    try:
        from models.medclip_model import medclip
        medclip.load()
    except Exception as e:
        logger.error(f"[STARTUP] Failed to load MedCLIP: {e}")
        raise RuntimeError(f"MedCLIP load failed: {e}")

    try:
        from models.medblip_model import medblip
        medblip.load()
    except Exception as e:
        logger.error(f"[STARTUP] Failed to load MedBLIP: {e}")
        raise RuntimeError(f"MedBLIP load failed: {e}")

    logger.info("[STARTUP] All models loaded and ready.")
