import os
import matplotlib.pyplot as plt


def create_chart(data) -> str:
    try:
        if not data:
            raise ValueError("Data list is empty.")
        
        plt.figure(figsize=(10, 5))
        plt.bar(range(len(data)), data, color='b')
        plt.title('Transaction Amounts')
        plt.xlabel('Transaction Index')
        plt.ylabel('Amount')
        plt.grid(True, axis='y')

        graph_file = "chart.png"
        plt.savefig(graph_file)
        plt.close()
        
        if not os.path.exists(graph_file):
            raise FileNotFoundError("Graph file was not created.")
        return graph_file
    except Exception as e:
        print(f"Error creating chart: {e}")
<<<<<<< HEAD
        return None
    



def create_chart_by_total(data: list[dict]) -> str:
    labels = [list(item.keys())[0] for item in data]
    values = [list(item.values())[0] for item in data]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='b')
    plt.title('Transaction Amounts')
    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.grid(axis='y')


    graph_file = "chart.png"
    plt.savefig(graph_file)
    plt.close()
    
    return graph_file
=======
        return None
>>>>>>> 01be670db25303917b43e4c0b24677c0e8b2d9c4
