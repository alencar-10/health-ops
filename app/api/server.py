import sys
import asyncio

if sys.platform.startswith("win"):
    from asyncio import WindowsSelectorEventLoopPolicy
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from app.review.review_queue import ReviewQueue
from app.domain.drug import Drug

from app.bootstrap.application import create_application

app = FastAPI()

queue = ReviewQueue()

creator = None


# -------------------------
# STARTUP
# -------------------------

@app.on_event("startup")
async def startup():

    global creator

    creator = await create_application()


# -------------------------
# ENDPOINTS
# -------------------------

@app.get("/reviews")
def list_reviews():

    return queue.list_pending()


@app.post("/approve/{item_id}")
def approve(item_id: int):

    items = queue.load()

    item = None

    for i in items:
        if i["id"] == item_id:
            item = i
            break

    if not item:
        return {"error": "item not found"}

    drug_data = item["drug"]

    drug = Drug(item["descricao_original"])

    drug.principles = [drug_data["principle"]]
    drug.strengths = [drug_data["strength"]]
    drug.form = drug_data["form"]

    drug.principle = drug_data["principle"]
    drug.codforma = None
    drug.normalized = item["descricao_original"]

    # -------------------------
    # CRIAR NO ERP
    # -------------------------

    product = creator.create(drug)

    # -------------------------
    # MARCAR APROVADO
    # -------------------------

    queue.approve(item_id)

    return {
        "status": "approved",
        "product": product
    }