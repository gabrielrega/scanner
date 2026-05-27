It seems the issue persists and is related to your Docker setup or user permissions on your machine, which is outside of my control as an agent. The error `the docker client must be run with elevated privileges to connect` specifically indicates that the Docker daemon is either not running, or your current user account does not have the necessary permissions to communicate with it.

To resolve this, please follow these steps:

1.  **Ensure Docker Desktop is Running**: Make sure the Docker Desktop application is actively running on your Windows machine. You should see the Docker icon in your system tray.
2.  **Verify User Permissions**: On Windows, your user account needs to be part of the `docker-users` security group to interact with Docker without elevated privileges.
    *   Search for "Computer Management" in your Windows search bar and open it.
    *   Navigate to `Local Users and Groups` -> `Groups`.
    *   Double-click on `docker-users`.
    *   Ensure your user account is listed there. If not, you'll need to add it and then restart your computer.
3.  **Run Terminal as Administrator**: Even if you are in the `docker-users` group, sometimes Docker requires the terminal (PowerShell or Command Prompt) to be run with elevated privileges.
    *   Right-click on your terminal application icon.
    *   Select "Run as administrator."
4.  **Try `docker-compose up` Again**: From the elevated terminal, navigate to your project directory (`C:\Users\Gabriel\OneDrive\__Projetos\scanner\`) and run:
    ```bash
    docker-compose up --build -d
    ```

**Until this fundamental Docker connectivity issue is resolved on your machine, I will be unable to execute any Docker-related commands or tests.** Please let me know once you have successfully gotten `docker-compose up --build -d` to run without errors from your end.