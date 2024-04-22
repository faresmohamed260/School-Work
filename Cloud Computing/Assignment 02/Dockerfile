# Use the Official Jupyter Docker image as the base image
FROM jupyter/datascience-notebook

# Set the working directory inside the container
WORKDIR /app

# Copy the Jupyter Notebook file from your local machine to the container
COPY Assignment_02.ipynb /app/Assignment_02.ipynb
COPY books.csv /app/books.csv

# Expose the port Jupyter Notebook runs on
EXPOSE 8888

# Command to run Jupyter Notebook when the container launches
CMD ["jupyter", "notebook", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root"]
