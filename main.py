from agent import *
from langchain_core.messages import HumanMessage


def main():
    response=graph.invoke(
        {"messages": [HumanMessage(' what is the location of the company. also please show me the reservations')]})
    last_message = response["messages"][-1]
    print(last_message.content)

if __name__ == "__main__":
    main()
