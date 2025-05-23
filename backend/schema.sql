DROP TABLE IF EXISTS notes;

CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    is_important BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO notes (title, content, subject, is_important) VALUES
('Grocery List', 'Milk, Eggs, Bread, Cheese', 'Personal', 0),
('Meeting Notes', 'Discuss project timeline and deliverables.', 'Work', 1),
('Book Ideas', 'A sci-fi novel about time travel.', 'Creative', 0);