import os


def select_recovery_algorithm():
    while True:
        # Display the menu for the user to select an algorithm
        print("Select a retrieval algorithm:")
        print("1: Boolean Retrieval")
        print("2: Okapi BM25")
        print("3: Vector Space Model")

        choice = input("Enter the number of the algorithm (1-3): ")

        if choice == '1':
            # User selects Boolean Retrieval
            print("\nYou selected Boolean Retrieval.")
            query_entry = input("Enter your query: ")  # Prompt user for query
            # Call the Boolean Retrieval script and pass the query
            os.system(f'python recovery_algorithms/boolean_retrieval.py "{query_entry}"')
        elif choice == '2':
            # User selects Okapi BM25
            print("\nYou selected Okapi BM25.")
            query_entry = input("Enter your query: ")  # Prompt user for query
            # Call the Okapi BM25 script and pass the query
            os.system(f'python recovery_algorithms/okapi_bm25.py "{query_entry}"')
        elif choice == '3':
            # User selects Vector Space Model
            print("\nYou selected Vector Space Model.")
            query_entry = input("Enter your query: ")  # Prompt user for query
            # Call the Vector Space Model script and pass the query
            os.system(f'python recovery_algorithms/vector_space_model.py "{query_entry}"')
        else:
            print("Invalid choice, please select a number between 1 and 3.")

        # Ask if the user wants to run another query
        repeat = input("\nDo you want to run another query? (y/n): ")
        if repeat.lower() != 'y':
            break


if __name__ == "__main__":
    select_recovery_algorithm()
