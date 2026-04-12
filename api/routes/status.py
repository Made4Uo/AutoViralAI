from fastapi import APIRouter, Depends, Request

from api.routes import verify_api_key

router = APIRouter()


@router.get("/status")
async def get_status(request: Request, _=Depends(verify_api_key)):
    orchestrator = getattr(request.app.state, "orchestrator", None)

    if orchestrator is None:
        return {
            "status": "starting",
            "pipelines": {"creation": "unknown", "learning": "unknown"},
            "stats": {},
        }

    jobs = orchestrator.get_scheduled_jobs()

    return {
        "status": "running",
        "pipelines": {
            "creation": {
                "cycles_completed": orchestrator.creation_cycle,
            },
            "learning": {
                "cycles_completed": orchestrator.learning_cycle,
            },
        },
        "scheduled_jobs": jobs,
        "stats": {
            "target_followers": orchestrator.settings.target_followers,
        },
    }
