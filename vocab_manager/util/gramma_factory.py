from pydantic import BaseModel, create_model

def GrammaModelFactory(config: str) -> BaseModel:
    if config == "substantive":
        fields = {
            "gender": (str, None),
            "nominative": (list[str]),
            "genitive": (list[str]),
            "dative": (list[str]),
            "accusative": (list[str]),
            "vocative": (list[str]),
            "locative": (list[str]),
            "instrumental": (list[str])
            }
    elif config == "verb":
        fields = {
            "word": (str, ...),
            "definition": (str, ...),
            "part_of_speech": (str, None),
            "synonyms": (list[str], []),
        }
    else:
        raise ValueError(f"Unknown config: {config}")

    return create_model("Gramma", **fields)


Substantive = GrammaModelFactory("substantive")
Verb = GrammaModelFactory("verb")

# # Example usage:
# substantive_instance = Substantive(
#     nominative=["lednička","ledničky"],
#     genitive=["",""],
#     dative=["",""],
#     accusative=["ledničku","ledničky"],
#     vocative=["",""],
#     locative=["ledničce",""],
#     instrumental=["",""]
#     )

# print(substantive_instance)

