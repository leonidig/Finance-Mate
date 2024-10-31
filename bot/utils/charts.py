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
        return None