from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from bson import ObjectId


class Product(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    name: str
    price: float
    description: Optional[str] = None
    stock: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class ProductDBModel(Product):
    def model_dump(
        self,
        *,
        mode="python",
        include=None,
        exclude=None,
        context=None,
        by_alias=None,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        round_trip=False,
        exclude_computed_fields=False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback=None,
        serialize_as_any=False,
    ):
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            exclude_computed_fields=exclude_computed_fields,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )
        if self.id:
            data["_id"] = str(data["_id"])
        return data


def fix_product(product):
    product["id"] = str(product.pop("_id")) if "_id" in product else None
    return product


# Example: define products_cursor as an empty list or fetch from your database
products_cursor = []

products_list = [
    ProductDBModel(**fix_product(product)).model_dump() for product in products_cursor
]


class UpdateProdcut(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None
