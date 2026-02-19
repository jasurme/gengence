from fastmcp import FastMCP
from datetime import datetime
mcp = FastMCP(name="CurrentTime")

@mcp.tool()
def get_current_time(format: str)->str:
    "get current time"
    now = datetime.now()
    try: 
        return now.strftime(format)
    except:
        raise ValueError("please enter valid format")


if __name__ == "__main__":

    mcp.run()

# print(get_current_time("%Y-%m-%d %H:%M:%S"))