# Adobe Hackathon - Round 1A Submission

This project is a solution for Round 1A of the Adobe Hackathon, "Understand Your Document". It provides a fast, offline, and containerized solution to extract a structured outline (Title, H1, H2, H3) from a PDF document.

### **Approach**

The solution uses a lightweight, heuristic-based approach to analyze the PDF structure without relying on large machine learning models. The core logic is as follows:

1.  **Dominant Font Analysis**: The script first analyzes the entire document to find the most common font size, which is assumed to be the body text.
2.  **Heuristic Scoring**: Each line of text is then scored based on a set of rules. A line gets a higher score if its font size is larger than the body text, if its font is bold, or if it follows common heading patterns (e.g., "1. Introduction", "Chapter 5").
3.  **Hierarchy Classification**: The lines that pass a certain score threshold are identified as heading candidates. The script then identifies the unique font sizes among these candidates and maps the top three largest sizes to H1, H2, and H3, respectively.
4.  **Title Extraction**: The document title is determined by finding the highest-scoring candidate on the first page.

This method is designed to be fast and efficient, meeting the strict performance requirements of the challenge.

### **Libraries Used**

- **`PyMuPDF`**: A high-performance Python library for PDF parsing and text extraction.

### **How to Build and Run**

**1. Build the Docker Image**
From the root directory of the project, run the following command:

```bash
docker build -t round1a-solution .
```
