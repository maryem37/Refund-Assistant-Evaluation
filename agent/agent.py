from models import model
from tools import calculate_right_refund , get_today_date
from tools import issue_refund_ticket,get_user_purchase_history
from dotenv import load_dotenv
from langchain.agents import create_agent
from prompts import agent_system_prompt
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from uuid import uuid4

load_dotenv()

agent = create_agent(
    model=model,
    system_prompt=agent_system_prompt,
    tools=[calculate_right_refund,get_user_purchase_history,issue_refund_ticket,get_today_date],
    checkpointer=InMemorySaver()
)

def run_conversation():
    config = {"configurable": {"thread_id": str(uuid4())}}

    text = "I would like to request a refund"
    print(text)
    
    question = HumanMessage(content=text)
    conversation = True

    while conversation:

        response = agent.invoke({"messages":question}, config=config)
        last_message = response["messages"][-1]
        print(last_message.content)
        conversation = False

        if conversation:
            user_input = input("reply: \n")
            question = HumanMessage(content=user_input)

    print("the job is done!")

#if __name__ == "__main__":
 #   run_conversation()