import csv
from collections import defaultdict
import ast

keyword_groups = {
    "Natural Language Processing": [
        "Grammar", "Dictionaries", "Decision making", "Decoding", "Error analysis", "Encoding", "Knowledge based systems", 
        "Knowledge discovery", "Knowledge engineering", "Knowledge transfer", "Labeling", "Learning (artificial intelligence)", 
        "Learning systems", "Text-to-image synthesis", "Natural language processing", "Natural languages", "Linguistics", "Message passing", "Inference algorithms", 
        "Markov processes", "Markov random fields", "Mixture models", "Pragmatics", "Prediction algorithms", "Predictive models", "Probabilistic logic",
        "Semantics", "Search problems", "Sequential analysis", "Supervised learning", "Vocabulary", "Text recognition", "Syntactics", "Taxonomy",
    ],
    "Medical Imaging and Healthcare": [
        "Medical imaging", "Biomedical imaging", "Computed tomography", "Cancer", 
        "Biomedical optical imaging", "Disease diagnosis", "Blood vessels", "Bones",
        "Diseases", "Biomedical imaging", "Disease diagnosis", "X-ray imaging",
        "Medical diagnostic imaging", "Magnetic resonance imaging", "Lesions", "Liver",
        "Positron emission tomography", "Pancreas", "Pathology", "Retina", "Medical diagnostic imaging",
        "Genomics", "Mel frequency cepstral coefficient", "Optical imaging", "Optical filters", 
        "Optical propagation", "Optical scattering", "Picture archiving and communication systems", "Prognostics and health management"
    ],
    "Autonomous Vehicles and Robotics": [
        "Autonomous driving", "Autonomous automobiles", "Autonomous vehicles", 
        "Robotics", "Automation", "Aerospace electronics", "Path planning", 
        "SLAM", "Collision avoidance", "Navigation", "UAVs", "Drone vision", 
        "Aerial vehicle navigation", "Remote inspections", 
        "Swarm intelligence", "Autonomous systems",
        "Automobiles", "Autonomous vehicles", "Robotics", "Path planning", "Navigation", 
        "UAVs", "Drone vision", "Aerial vehicle navigation",
        "Engines", "Humanoid robots", "Marine vehicles", "Legged locomotion", "Manipulators",
        "Robot sensing systems", "Robot vision systems", "Robots", "Simultaneous localization and mapping", "Motion compensation", 
        "Motion estimation", "Object detection", "Object recognition", "Object segmentation", "Object tracking", 
        "Robot vision systems", "Unmanned aerial vehicles", "Vehicle dynamics", "Vehicles", "Visual odometry", "Visual perception", "Visual systems"
    ],
    "Human-Centric Vision": [
        "Activity recognition", "Human pose estimation", "Gesture recognition", 
        "Facial recognition", "Emotion analysis", "Gait analysis", "Cognition", 
        "Assistive technology", "Creativity",
        "Emotion recognition", "Gesture recognition", "Facial recognition", "Cognition",
        "Face recognition", "Facial features", "Gaze tracking", "Face", "Facial recognition", "Head", "Lips",
        "Mouth", "Hip", "Neck", "Muscles", "Hippocampus", "Psychology", "Hair", "Microphones", "Nose",
        "Elbow", "Ear", "Skin", "Torso", "Wrist"
    ],
    "Natural Scenes and Environmental Analysis": [
        "Agriculture", "Atmospheric measurements", "Atmospheric modeling", 
        "Clouds", "Remote sensing", "Ocean monitoring", "Aerial imagery", 
        "Satellite images", "Climate analysis",
        "Agriculture", "Atmospheric measurements", "Clouds", "Ocean monitoring", "Climate analysis",
        "Geophysical measurement techniques", "Ground penetrating radar", "Extraterrestrial measurements", "Meteorology",
        "Rain", "Rivers", "Snow", "Roads", "Public transportation", "Geophysical measurement techniques", 
        "Acoustics", "Animals", "Birds", "Clutter", "Liquids", "Monitoring", "Pipelines", "Powders", "Photonics",
        "Satellites", "Sensors", "Sensor arrays", "Spatial resolution", "Spatial coherence", 
        "Vegetation", "Urban areas", "Water resources"
    ],
    "Augmented Reality (AR) and Virtual Reality (VR)": [
        "Augmented reality", "Virtual reality", "3D reconstruction", 
        "Avatars", "Holography", "Immersive environments",
        "3D reconstruction", "Immersive environments",
        "Graphics", "Graphics processing units",
        "Rendering (computer graphics)", "Virtual reality", "3D reconstruction", "Immersive environments",
        "Three-dimensional displays", "Two dimensional displays"
    ],
    "Video Analysis and Action Recognition": [
        "Video processing", "Motion segmentation", "Event detection", 
        "Temporal analysis", "Video summarization", "Action recognition",
        "Motion segmentation", "Event detection", "Video summarization", "Action recognition",
        "Image recognition", "Image segmentation", "Image matching", "Image resolution", "Image retrieval", "Image restoration",
        "Motion pictures", "Pattern recognition", "Pose estimation", "Saliency detection", "Motion compensation", "Motion estimation",
        "Joints", "Junctions", "Kinematics", "Kinetic theory",  "Message passing", "Monitoring",
        "Structure from motion", "Streaming media",
        "Target recognition", "Target tracking", "Tracking", "Video surveillance", "Video sequences", "Videos", "Video compression"   
    ],
    "Generative Models and Creativity": [
        "GANs", "Image generation", "Style transfer", "Artistic applications", 
        "Artificial intelligence", "Boosting", 
        "Brain modeling", "Artificial neural networks",
        "Art", "Boosting", "Artificial neural networks",
        "Generative adversarial networks", "Image generation", "Image representation",
        "Painting", "Paints", "Multimedia communication", "Art", "Generative adversarial networks"
    ],
    "Security and Surveillance": [
        "Surveillance systems", "Anomaly detection", "Crowd monitoring", 
        "Camera networks", "License plate recognition", "Security applications", 
        "Alarm systems", "Broadcasting",
        "Surveillance systems", "Anomaly detection", "Camera networks", "License plate recognition", "Security applications",
        "Forensics", "Forgery", "Face recognition", "Image registration", "Image quality", "Image sensors",
        "Privacy", "Security", "Search engines", "Protocols", "Forensics", "Forgery", "Anomaly detection",
        "Surveillance", "Video surveillance"
    ],
    "Scene Understanding and Reconstruction": [
        "Scene segmentation", "Semantic segmentation", "Depth estimation", 
        "Scene parsing", "Clustering algorithms", "Clustering methods", 
        "Context modeling", "3D reconstruction",
        "Scene segmentation", "Depth estimation", "3D reconstruction",
        "Image segmentation", "Image reconstruction", "Image denoising", "Image decomposition", "Image edge detection",
        "Image analysis", "Image segmentation", "Object detection", "Object segmentation", "Scene parsing", "Scattering", 
        "Active contours", "Apertures", "Measurement", "Optical detectors", "Optical losses", 
        "Optical computing", "Optical distortion", "Optical sensors", "Optical surface waves", 
        "Optical variables control", "Optical wavelength conversion", "Refractive index",
        "Surface reconstruction", "Surface morphology", "Surface texture", "Surface treatment", "Surface acoustic waves",
        "Skeleton", "Surface waves"
    ],
    "Vision for Social Good": [
        "Accessibility", "Wildlife monitoring", "Disaster management", 
        "Social media analysis", "Assistive technology", "Crowdsourcing",
        "Wildlife monitoring", "Disaster management", "Social media analysis",
        "Market research", "Social media analysis", "Location awareness", "Disaster management",
        "Social network services", "Disaster management", "Wildlife monitoring", "Crowdsourcing", "Crowd monitoring"
    ],    
    "Datasets and Benchmarks": [
        "Large-scale datasets", "Benchmark testing", "Vision datasets", 
        "Training techniques", "Evaluation protocols", "Dataset creation",
        "Large-scale datasets", "Benchmark testing", "Vision datasets",
        "Image databases", "Indexes", "Indexing", "Training data"
    ],
    "Tools and Frameworks": [
        "Toolkits", "OpenCV", "Software tools", "Hardware tools", 
        "Development frameworks", "Programming libraries",
        "Software tools", "Hardware", 
        "Adaptive optics",  "Memory management", "Memory modules", "Network architecture", "Network topology", 
        "Next generation networking", "Neural networks", "Neurons", "Microprocessors", 
        "Minimization methods", "Parallel processing", "Peer-to-peer computing", "Routing", "Registers", "Real-time systems",
        "Software", "Servers", "Runtime", "Stacking",  "Tools", "Web services"
    ],
    "Data Collection and Management": [
        "Data collection", "Data mining", "Data models", 
        "Data acquisition", "Metadata", "Annotation tools",
        "Data collection", "Data mining", "Data models", "Data acquisition", "Metadata", "Annotation tools",
        "Data models", "Data acquisition", "Metadata", "Annotation tools",
        "Merging", "Probes", "Random access memory", "Random variables",
         "Sampling methods", "Sorting", "Tagging", "Testing", "Task analysis", "Training"
    ],
    "Core Vision Algorithms": [
        "Feature extraction", "Image processing", "Convolution", 
        "Convolutional neural networks", "Computational modeling", 
        "Clustering algorithms", "Semantic segmentation",
        "Frequency-domain analysis", "Image color analysis", "Image matching", "Frequency division multiplexing",
        "Pattern matching", "Image edge detection", "Image registration", "Reconstruction algorithms",
        "Adaptive systems", "Bayes methods", "Backpropagation", "Convolutional codes",
        "Frequency selective surfaces", "Image annotation", "Image coding", "Imaging", "Iterative closest point algorithm", 
        "Iterative methods", "Kernel", "Level set", "Inference algorithms", "Markov processes", "Markov random fields", "Mixture models"
        "Prediction algorithms", "Predictive models", "Quantization (signal)", "Rate distortion theory", "Rate-distortion",
        "Support vector machines", "Self-organizing feature maps",
        "Transform coding", "Transforms", "Viterbi algorithm", "Recurrent neural networks"
    ],
    "Mathematical Foundations": [
        "Optimization techniques", "Closed-form solutions", 
        "Approximation algorithms", "Computational complexity", 
        "Covariance matrices", "Algebra",
        "Optimization techniques", "Closed-form solutions", "Approximation algorithms", "Computational complexity", "Covariance matrices",
        "Covariance matrices", "Entropy", "Estimation", "Extrapolation", "Euclidean distance", "Laplace equations", 
        "Maximum likelihood estimation", "Matrix decomposition", "Linear approximation", "Linear systems", 
        "Linear programming", "Linear matrix inequalities", "Monte Carlo methods",
        "Optimization methods", "Quadratic programming", "Parametric statistics", "Probability", "Probability density function", 
        "Probability distribution", "Principal component analysis", "Inverse problems", "Perturbation methods", "Optimization",
        "Acceleration", "Adaptation models", "Channel capacity", "Chebyshev approximation",
        "Graph theory", "Graphical models", "Geometry", "Jacobian matrices", 
        "Mathematical model", "Method of moments", "Minimization",
        "Manifolds", "Numerical models", "Probabilistic logic", "Quaternions", "Random variables", "Differential equations",
        "Finite element analysis", "Radon", "Sparse matrices", "Stochastic processes", "Semisupervised learning", "Semantics",
        "Symmetric matrices", "Transfer functions", "Tree graphs", "Upper bound"
    ],
    "Signal and Statistical Processing": [
        "Correlation", "Covariance matrices", "Noise reduction", 
        "Bayesian methods", "Statistical models",
        "Correlation", "Covariance matrices", "Noise reduction", "Bayesian methods", "Statistical models",
        "Bayesian methods", "Noise reduction", "Statistical models", "Gaussian distribution", "Gaussian mixture model", 
        "Gaussian noise", "Gaussian processes", "Kalman filters", "Hidden Markov models", "Filtering", "Frequency modulation",
        "Noise measurement", "Noise robustness", "Signal resolution", "Signal to noise ratio", "Mutual information", 
        "Gaussian distribution", "Gaussian noise", "Bayesian methods", "Statistical models", "Kalman filters", 
        "Hidden Markov models", "Frequency modulation", "Gaussian mixture model",
        "Absorption", "Acceleration", "Attenuation", "Bandwidth", "Bit error rate", "Bit rate",
        "Histograms", "Interference", "Interpolation",
        "Loss measurement", "Nonlinear distortion", "Nonlinear optics", "Modulation",
        "Optimized production technology", "Power demand", "Potential energy", "Redundancy",
        "RF signals", "Radio frequency", "Spectral analysis", "Spectrogram", "Sensitivity", "Smoothing methods",
        "Source separation", "Wavelet domain", "Wavelet transforms"
    ],
    "Industrial and Manufacturing Applications": [
        "Quality control", "Factory automation", "Defect detection", 
        "Assembly line monitoring", "Industrial vision", "Batch production systems", 
        "Buildings", "Architecture", "Bridges",
        "Quality control", "Factory automation", "Defect detection", "Industrial vision", "Batch production systems"   ,
        "Flyback transformers", "Micromechanical devices", "Laser modes", "Laser radar", "Lasers", "Integrated circuits", 
        "Integrated optics", "Geometrical optics", "Electronics packaging",
        "Quality assessment", "Quality control", "Factory automation", "Defect detection", "Industrial vision", 
        "Batch production systems", "Particle measurements", "Particle separators", "Printing", "Micromechanical devices", 
        "Laser radar", "Flyback transformers", "Integrated circuits", "Laser modes", "Laser radar", "Resists", 
        "Geometrical optics", "Integrated optics", "Electronics packaging", "Geophysical measurement techniques",
        "Additives", "Aggregates", "Generators", "Industries", "Lenses", "Manganese", "Mirrors",  "Ovens", "Periodic structures", "Photonics",
        "Proposals", "Prototypes", "Surface cleaning", "Switched mode power supplies", "Silicon", "Silicon carbide",
        "Toy manufacturing industry", "Technological innovation", "Variable speed drives", "Tires"
    ],
    "Ethics and Fairness in Vision": [
        "Fairness in AI", "Bias in datasets", "Ethical AI", 
        "Privacy in vision systems", "Explainable AI",
        "Intellectual property"       
    ],
    "Miscellaneous": [
        "Asia", "Australia", "Europe", "Facebook", "Flickr", "Google", "Microsoft Windows", "Mobile handsets", "Fans", 
        "Feeds", "Feedback loop", "Fuses", "Gallium nitride", "Games", "Grippers", "Grounding", "Gyroscopes", "Hafnium", 
        "Hamming distance", "Handheld computers", "Harmonic analysis", "Heating systems", "Heuristic algorithms", 
        "Aging", "Bicycles", "Bidirectional control", "Binary codes", "Bioinformatics", "Biological neural networks", 
        "Biological system modeling", "Bipartite graph", "Clocks", "Cloning", "Clothing", "Cloud computing", 
        "Codecs", "Coherence", "Collaboration", "Color", "Colored noise", "Compounds", "Computational efficiency", 
        "Computer architecture", "Computer science", "Computer vision", "Computers", "Containers", "Controllability", 
        "Convergence", "Convex functions", "Analytical models", "Annealing", "Azimuth", "Bars", "Best practices", "Calibration", 
        "Cameras", "Cams", "Cascading style sheets", "Cats", "Complexity theory", "Cost function", "Couplings", "Cows", "DSL", 
        "Data structures", "Databases", "Deconvolution", "Decorrelation", "Deformable models", 
        "Degradation", "Delays", "Detection algorithms", "Detectors", 
        "Dimensionality reduction", "Discrete cosine transforms", "Dispersion", "Distortion", "Distribution functions", 
        "Dogs", "Dynamic range", "Dynamic scheduling", "Dynamics", "Eigenvalues and eigenfunctions", 
        "Electroencephalography", "Electron tubes","Encyclopedias", "Explosives", 
        "Facsimile", "Focusing", "Footwear",
        "Forecasting", "Glass", "Gold", "Graphite", "Gravity", "Gray-scale", 
        "History", "Hyperspectral imaging", "ISO", "Indoor environments", "Ink", "Ions", "Iron", "Jitter", 
        "Lattices", "Layout", "Light sources", "Lighting", "Logistics", "Logic gates", "Manganese", "Manuals", "Nickel", "Machine learning",
        "Physics", "Planning", "Reliability", "Robustness",
        "Space heating", "Standards", "Standardization", "Scalability", "Schedules", "Search problems", "Shape", 
        "Shortest path problem", "Strain", "Spirals", "Splines (mathematics)", "Switches",
        "Synchronization", "Tensile stress", "Time factors", "Time measurement", "Topology", 
        "Transmission line matrix methods", "Tuning", "UHDTV", "Uncertainty", "Wiring", "Xenon", "Zinc", "Zirconium",
        "Optical fiber networks", "Optical network units", "Smart phones", "Solid modeling", "Spatiotemporal phenomena",
        "TV", "Trajectory", "Unsupervised learning", "Visualization", "Watermarking" , "Windows", "Wireless communication", "YouTube"
    ]
}

def process_csv(file_path):
    # Dictionaries to store counts
    grouped_counts = defaultdict(lambda: {"total": 0, "company": 0, "university": 0})

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Check if "ieee_keywords" section is empty
            if not row.get('ieee_keywords'):
                continue

            # Extract company affiliation percentage
            company_affiliation = float(row['company_affiliation'])

            # Determine if the paper is company or university
            is_company = company_affiliation > 0

            # Extract keywords from the "ieee_keywords" column
            keywords = ast.literal_eval(row['ieee_keywords'])  # Convert string list to actual list

            for keyword in keywords:
                for group, group_keywords in keyword_groups.items():
                    if keyword in group_keywords:
                        grouped_counts[group]["total"] += 1
                        if is_company:
                            grouped_counts[group]["company"] += 1
                        else:
                            grouped_counts[group]["university"] += 1

    return grouped_counts

def write_results_to_file(keyword_counts, output_file):
    with open(output_file, 'w') as f:
        f.write(f"{'Keyword':<30} {'Total Papers':<15} {'Company Papers':<15} {'University Papers':<15}\n")
        f.write("-" * 75 + "\n")
        for keyword, counts in sorted(keyword_counts.items(), key=lambda x: x[0]):
            f.write(f"{keyword:<30} {counts['total']:<15} {counts['company']:<15} {counts['university']:<15}\n")
            
def extract_unique_keywords(file_path, output_file):
     # Flatten the keyword_groups dictionary into a set of grouped keywords
    grouped_keywords = set(keyword for group in keyword_groups.values() for keyword in group)
    
    unmatched_keywords = set()  # Use a set to store unique unmatched keywords

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Check if "ieee_keywords" section is empty
            if not row.get('ieee_keywords'):
                continue

            # Extract keywords as a list
            try:
                keywords = ast.literal_eval(row['ieee_keywords'])  # Convert string list to actual list
                for keyword in keywords:
                    if keyword not in grouped_keywords:
                        unmatched_keywords.add(keyword)  # Add unmatched keywords to the set
            except (ValueError, SyntaxError):
                # Skip rows with invalid keyword formatting
                continue

    # Write unmatched keywords to the output file
    with open(output_file, 'w') as outfile:
        for keyword in sorted(unmatched_keywords):  # Sort keywords alphabetically
            outfile.write(keyword + '\n')

# Replace 'your_file.csv' with the path to your CSV file
file_path = '/Users/merve/Data_Literacy-1/data/iccv_preprocessed/iccv2021.csv'
output_file = '/Users/merve/Data_Literacy-1/data//iccv_preprocessed/results_21.txt'
keyword_file = '/Users/merve/Data_Literacy-1/data//iccv_preprocessed/keywords_21.txt'
extract_unique_keywords(file_path, keyword_file)
keyword_counts = process_csv(file_path)
write_results_to_file(keyword_counts, output_file)
