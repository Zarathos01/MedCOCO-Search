### Medical Image Fusion & Processing

Converting DICOM series into high-quality JPEG representations using a **Weighted Center-Slice Fusion** approach. 

Below is a concise breakdown of the methodologies considered and why the current implementation was chosen.

------

## 1. Methodology: Weighted Center-Slice Fusion (Current)

This approach identifies the middle of a scan volume s2 and its immediate neighbors s1, s3. It applies a weighted average using the formula:

![image-20260504205820444](C:\Users\Mohamed\AppData\Roaming\Typora\typora-user-images\image-20260504205820444.png)

### Why it is the Best Approach

- **Noise Reduction:** By blending three consecutive slices, random digital noise is mathematically reduced without losing anatomical detail.
- **Anatomical Integrity:** Since it only uses a 3-slice "window," it avoids the "ghosting" or blurring effect that occurs when blending distant slices with different anatomy.
- **Simulation of "Thick Slices":** It mimics professional radiological "thick-slab" viewing, which provides a smoother, more interpretable image for both humans and AI models.
- **Broadcasting Safety:** The script includes an automated resizing check, ensuring that even if slices have slightly different dimensions, they are aligned before fusion.

------

## 2. Alternative Approaches Considered

### A. Simple Averaging (Mean)

- **Method:** Taking the average of every pixel across the entire series (e.g., all 20 images).
- **Disadvantage:** Causes extreme blurring. As anatomy changes through the scan (e.g., moving through the lungs), overlapping every slice creates a "foggy" image where no single structure is sharp.

### B. Maximum Intensity Projection (MIP)

- **Method:** Keeping only the brightest pixel at every coordinate across the stack.
- **Disadvantage:** Excellent for bone and metal (stents), but it destroys soft tissue contrast. For brain or joint scans, the resulting image looks flat and lacks diagnostic depth.

### C. First-Mid-Last Fusion

- **Method:** Blending the absolute first, middle, and last images of a folder.
- **Disadvantage:** Results in a "transparent sandwich" effect. Because the first and last slices are often inches apart, the fused result shows multiple body parts stacked on top of each other, making it useless for analysis.

------

## 3. Comparative Summary

| **Feature**         | **Weighted Center (Current)** | **Full Average**       | **MIP**               |
| ------------------- | ----------------------------- | ---------------------- | --------------------- |
| **Sharpness**       | **Excellent**                 | Very Poor (Blurry)     | High (Brights only)   |
| **Noise Level**     | Low                           | **Lowest**             | Moderate              |
| **Ghosting Effect** | None                          | High                   | High                  |
| **Best Use Case**   | **General Diagnostic / AI**   | Low-dose noise cleanup | Stents, Bone, Vessels |

------

## 4. Key Features of the Script

- **Hybrid Ingestion :** Seamlessly processes **both standard folders and compressed `.zip`** archives in a single run.
- **Unicode Support:** Uses `imdecode` and `imencode` to handle file paths with special characters (e.g., "Köhler").
- **Path Safety:** Automatically shortens long DICOM UIDs and sanitizes filenames to bypass Windows 260-character path limits and illegal character errors.
- **Recursive Discovery:** Uses deep-tree scanning (`os.walk`) to find DICOMs or JPEGs even if they are buried in multiple sub-directory layers.
- **Structure Flattening:** Dumps all final fused results into a single directory for easy AI training or review, while preserving metadata via descriptive filenames.
- **Failure Logging:** Generates a `fusion_log.txt` to track empty folders, unreadable files, or successful writes.

------

## 5. How to Run

The processing pipeline consists of two stages: extraction and fusion.

1. **Extract & Sort:** Convert raw DICOM files into an ordered JPG directory structure.

   Bash

   ```
   python dcm2jpg_ordered.py
   ```

2. **Fuse & Dump:** Perform the weighted fusion and collect all results into the final output folder.

   Bash

   ```
   python final_jpg.py
   ```