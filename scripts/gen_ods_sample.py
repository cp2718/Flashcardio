import argparse
import os
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P
from odf.style import Style, TableProperties, TableColumnProperties

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate sample ODS file with flashcards.')
parser.add_argument('-o', '--output', type=str, default='samples/sample.ods',
                    help='Output ODS file path (default: samples/sample.ods)')
args = parser.parse_args()

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(args.output), exist_ok=True)

# Initialize document
doc = OpenDocumentSpreadsheet()

# Add basic styles
table_style = Style(name="TableStyle", family="table")
table_style.addElement(TableProperties(align="center"))
doc.automaticstyles.addElement(table_style)

column_style = Style(name="ColumnStyle", family="table-column")
column_style.addElement(TableColumnProperties(columnwidth="2.5in"))
doc.automaticstyles.addElement(column_style)

topics = {
    "Robotics": [
        ("actuator", "A device that converts energy into motion."),
        ("servo", "A motor with feedback for precise control of angular position."),
        ("sensor", "A device that detects or measures a physical property."),
        ("manipulator", "A mechanism used to interact with objects in the environment."),
        ("end effector", "The device at the end of a robotic arm, designed to interact with the environment."),
        ("autonomous", "Capable of operating without human intervention."),
        ("teleoperation", "Remote control of a robot by a human operator."),
        ("SLAM", "Simultaneous Localization and Mapping."),
        ("path planning", "The process of determining a route for a robot to follow."),
        ("kinematics", "The study of motion without considering forces."),
        ("inverse kinematics", "Calculating joint parameters to achieve a desired position of the end effector."),
        ("degrees of freedom", "The number of independent movements a robot can perform."),
        ("PID controller", "A control loop mechanism using proportional, integral, and derivative terms."),
        ("mobile robot", "A robot that can move in its environment."),
        ("humanoid", "A robot designed to resemble the human body."),
        ("swarm robotics", "The study of how large numbers of relatively simple robots can be designed to exhibit collective behavior."),
        ("ROS", "Robot Operating System, a flexible framework for writing robot software."),
        ("gripper", "A device used by robots to grasp and hold objects."),
        ("lidar", "A remote sensing method that uses light in the form of a pulsed laser to measure distances."),
        ("force sensor", "A device that measures the amount of force applied to an object."),
    ],
    "Machine Learning": [
        ("supervised learning", "Machine learning using labeled data."),
        ("unsupervised learning", "Machine learning using unlabeled data."),
        ("reinforcement learning", "Learning by trial and error, receiving rewards or penalties."),
        ("feature extraction", "The process of transforming raw data into input for a learning algorithm."),
        ("classification", "Assigning items to predefined categories."),
        ("regression", "Predicting a continuous value."),
        ("clustering", "Grouping similar data points together."),
        ("neural network", "A computational model inspired by the human brain."),
        ("deep learning", "Machine learning using neural networks with many layers."),
        ("activation function", "A function that determines the output of a neural network node."),
        ("loss function", "A function that measures the difference between predicted and actual values."),
        ("gradient descent", "An optimization algorithm for finding the minimum of a function."),
        ("overfitting", "When a model learns the training data too well, including noise."),
        ("underfitting", "When a model is too simple to capture the underlying pattern of the data."),
        ("cross-validation", "A technique for assessing how a model will generalize to an independent dataset."),
        ("training set", "The portion of data used to fit the model."),
        ("test set", "The portion of data used to evaluate the model."),
        ("validation set", "The portion of data used to tune the model's hyperparameters."),
        ("hyperparameter", "A parameter whose value is set before the learning process begins."),
        ("epoch", "One complete pass through the training dataset."),
    ],
    "Linear Algebra": [
        ("vector", "A quantity with both magnitude and direction."),
        ("matrix", "A rectangular array of numbers arranged in rows and columns."),
        ("scalar", "A single number."),
        ("transpose", "The operation of swapping the rows and columns of a matrix."),
        ("determinant", "A scalar value that can be computed from the elements of a square matrix."),
        ("eigenvalue", "A scalar associated with a linear system of equations that can be factored out when a linear transformation is applied."),
        ("eigenvector", "A nonzero vector that changes by only a scalar factor when that linear transformation is applied."),
        ("identity matrix", "A square matrix with ones on the diagonal and zeros elsewhere."),
        ("inverse matrix", "A matrix that, when multiplied by the original matrix, yields the identity matrix."),
        ("rank", "The dimension of the vector space generated by its columns."),
        ("system of equations", "A set of equations with the same variables."),
        ("linear transformation", "A function between two vector spaces that preserves vector addition and scalar multiplication."),
        ("orthogonal", "Vectors that are perpendicular to each other."),
        ("dot product", "An algebraic operation that takes two equal-length sequences of numbers and returns a single number."),
        ("cross product", "A binary operation on two vectors in three-dimensional space."),
        ("column space", "The set of all possible linear combinations of the column vectors of a matrix."),
        ("row space", "The set of all possible linear combinations of the row vectors of a matrix."),
        ("null space", "The set of all vectors that, when multiplied by the matrix, yield the zero vector."),
        ("LU decomposition", "The factorization of a matrix into a lower triangular matrix and an upper triangular matrix."),
        ("QR decomposition", "The factorization of a matrix into an orthogonal matrix and an upper triangular matrix."),
    ],
    "Weather Conditions": [
        ("humidity", "The amount of water vapor in the air."),
        ("dew point", "The temperature at which air becomes saturated with moisture and dew forms."),
        ("barometer", "An instrument measuring atmospheric pressure."),
        ("anemometer", "An instrument for measuring wind speed."),
        ("precipitation", "Any form of water that falls from clouds and reaches the ground."),
        ("front", "The boundary between two air masses."),
        ("cyclone", "A system of winds rotating inward to an area of low barometric pressure."),
        ("anticyclone", "A weather system with high atmospheric pressure at its center."),
        ("hurricane", "A type of storm called a tropical cyclone, which forms over tropical or subtropical waters."),
        ("tornado", "A rapidly rotating column of air that is in contact with both the surface of the Earth and a cumulonimbus cloud."),
        ("hail", "Precipitation in the form of balls or irregular lumps of ice."),
        ("fog", "A thick cloud of tiny water droplets suspended in the atmosphere at or near the earth's surface."),
        ("blizzard", "A severe snowstorm with high winds and low visibility."),
        ("drizzle", "Light rain falling in very fine drops."),
        ("gust", "A brief, strong rush of wind."),
        ("wind chill", "The lowering of body temperature due to the passing-flow of lower-temperature air."),
        ("UV index", "A measure of the strength of sunburn-producing ultraviolet radiation at a particular place and time."),
        ("microclimate", "The climate of a very small or restricted area."),
        ("barometric pressure", "The pressure exerted by the atmosphere at a given point."),
        ("cloud cover", "The fraction of the sky obscured by clouds."),
    ],
    "Software Engineering": [
        ("algorithm", "A step-by-step procedure for solving a problem or accomplishing a task."),
        ("API", "Application Programming Interface, a set of routines and protocols for building software."),
        ("bug", "An error or flaw in software that causes it to produce an incorrect or unexpected result."),
        ("class", "A blueprint for creating objects in object-oriented programming."),
        ("object", "An instance of a class."),
        ("inheritance", "The mechanism of basing an object or class upon another object or class."),
        ("encapsulation", "The bundling of data with the methods that operate on that data."),
        ("polymorphism", "The ability of different objects to respond in a unique way to the same message."),
        ("refactoring", "The process of restructuring existing computer code without changing its external behavior."),
        ("unit test", "A test that covers a small part of the application, usually a single function or method."),
        ("integration test", "A test that checks the interaction between different pieces of code."),
        ("agile", "A methodology based on iterative development, where requirements and solutions evolve through collaboration."),
        ("scrum", "An agile framework for managing work with an emphasis on software development."),
        ("kanban", "A scheduling system for lean and just-in-time manufacturing, also used in software development."),
        ("version control", "The management of changes to documents, computer programs, and other information."),
        ("repository", "A central location in which data is stored and managed."),
        ("merge", "The process of combining multiple sequences of changes into a single unified sequence."),
        ("branch", "A parallel version of a repository."),
        ("pull request", "A method of submitting contributions to a project."),
        ("continuous integration", "The practice of merging all developers' working copies to a shared mainline several times a day."),
    ]
}

for topic, pairs in topics.items():
    # Create table with style
    table = Table(name=topic, stylename="TableStyle")
    
    # Header row
    tr = TableRow()
    
    tc1 = TableCell()
    p1 = P(text="Word")
    tc1.addElement(p1)
    tr.addElement(tc1)
    
    tc2 = TableCell()
    p2 = P(text="Definition")
    tc2.addElement(p2)
    tr.addElement(tc2)
    
    table.addElement(tr)
    
    # Data rows
    for word, definition in pairs:
        tr = TableRow()
        
        tc_word = TableCell()
        p_word = P(text=word)
        tc_word.addElement(p_word)
        tr.addElement(tc_word)
        
        tc_def = TableCell()
        p_def = P(text=definition)
        tc_def.addElement(p_def)
        tr.addElement(tc_def)
        
        table.addElement(tr)
    
    doc.spreadsheet.addElement(table)

# Save the document
try:
    doc.save(args.output)
    print(f"Generated ODS file: {args.output}")
except Exception as e:
    print(f"Error saving ODS file: {e}")
    
    # Alternative: save as individual CSV files
    import csv
    csv_dir = "csv_files"
    os.makedirs(csv_dir, exist_ok=True)
    
    for topic, pairs in topics.items():
        csv_path = os.path.join(csv_dir, f"{topic.lower().replace(' ', '_')}.csv")
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Word", "Definition"])
            writer.writerows(pairs)
        print(f"Generated CSV file: {csv_path}")