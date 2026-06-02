FROM python:3.9

# Hugging Face Spaces require running as a non-root user
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the application files and change ownership to the non-root user
COPY --chown=user:user . /app

# Switch to the non-root user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Hugging Face Spaces exposes port 7860 by default
EXPOSE 7860

# Start the application using Uvicorn on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
