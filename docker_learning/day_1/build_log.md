**Build Log – Day 1: Container Shock**

**1. Difference between Image and Container (1 sentence):**
An image is a fixed blueprint of an application and its environment, while a container is a running instance created from that image.

**2. Why did you need `-p 8080:80` for nginx but not for python?**
I needed `-p 8080:80` for nginx because it runs a web server inside the container and I had to expose it to my browser, while Python was running interactively inside the container so it didn’t need any external access.

**3. What was the "shock" moment for you?**
The biggest shock was that the container could not access files from my computer and my computer could not access files from the container, which proved that containers are completely isolated environments.
