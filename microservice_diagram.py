from diagrams import Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.onprem.client import User
from diagrams.onprem.network import Internet
from diagrams.onprem.compute import Server

def get_architecture_description():
    print("Welcome to the Microservice Architecture Diagram Generator!")
    
    while True:
        try:
            num_services = int(input("How many microservices do you want to represent? "))
            if num_services < 1:
                raise ValueError("Number of microservices must be at least 1.")
            break
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid number.")
    
    service_names = []
    for i in range(num_services):
        service_name = input(f"Enter the name of microservice {i + 1}: ")
        service_names.append(service_name)
    
    has_db = input("Do you have a database in your architecture? (yes/no): ").lower() == "yes"
    has_load_balancer = input("Do you have a load balancer? (yes/no): ").lower() == "yes"
    
    return service_names, has_db, has_load_balancer

# Function to create the diagram based on user input
def generate_architecture_diagram(service_names, has_db, has_load_balancer):
    with Diagram("Microservice Architecture", show=False, outformat="png"):
        user = User("Client")
        internet = Internet("Internet Gateway")
        
        # Add the load balancer if user specified it
        if has_load_balancer:
            load_balancer = ELB("Load Balancer")
        else:
            load_balancer = internet
        
        # Create services
        services = []
        for service_name in service_names:
            service = ECS(service_name)
            services.append(service)
        
        # Add database if user specified it
        if has_db:
            database = RDS("Database")
            for service in services:
                service >> database
        
        # Connect services via load balancer or directly from internet
        user >> internet >> load_balancer >> services

# Main function to execute the program
if __name__ == "__main__":
    # Get architecture description from user
    service_names, has_db, has_load_balancer = get_architecture_description()
    
    # Generate the architecture diagram based on the description
    generate_architecture_diagram(service_names, has_db, has_load_balancer)
    print("Architecture diagram generated and saved as 'microservice_architecture.png'!")