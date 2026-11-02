from pydantic import BaseModel, Field

class answer(BaseModel):
    answer: str = Field( description="The answer that is needed for the user question.")
    conversation:bool = Field(description="this is an indicator to know if the conversation"\
                              "should still continu or no .if the agent has made thedecision about the refund this should be False"\
                                "if the conversation  still need more talk its True",default=True)

Answer = answer

class PurchaseItem(BaseModel):
    name: str = Field( description="The name of the item that the user purchased.")
