CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NUMERIC(5,2) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Types`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` NVARCHAR(160) NOT NULL,
    `multiplier` INTEGER NOT NULL
);

CREATE TABLE `Orders`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metalId` INTEGER NOT NULL,
    `styleId` INTEGER NOT NULL,
    `sizeId` INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_DATE,
    FOREIGN KEY (`metalId`) REFERENCES `Metals`(`id`),
    FOREIGN KEY (`styleId`) REFERENCES `Styles`(`id`),
    FOREIGN KEY (`sizeId`) REFERENCES `Sizes`(`id`)
);


-- Insert data into the 'styles' table
INSERT INTO styles (style, price) VALUES
    ('Classic', 500),
    ('Modern', 710),
    ('Vintage', 965);

-- Insert data into the 'sizes' table
INSERT INTO sizes (id, carets, price) VALUES
    (null, 0.5, 405),
    (null, 0.75, 782),
    (null, 1, 1470),
    (null, 1.5, 1997),
    (null, 2, 3638);

-- Insert data into the 'metals' table
INSERT INTO metals (id, metal, price) VALUES
    (null, 'Sterling Silver', 12.42),
    (null, '14K Gold', 736.4),
    (null, '24K Gold', 1258.9),
    (null, 'Platinum', 795.45),
    (null, 'Palladium', 1241);

-- Insert data into the 'types' table
INSERT INTO types (id, name, multiplier) VALUES
    (null, 'Ring', 1),
    (null, 'Earring', 2),
    (null, 'Necklace', 4);

-- Insert data into the 'orders' table
INSERT INTO Orders (metalId, styleId, sizeId) VALUES
    (1, 1, 1),
    (2, 2, 1),
    (4, 3, 1),
    (3, 2, 2),
    (1, 4, 2),
    (1, 1, 2),
    (1, 1, 3),
    (1, 1, 3),
    (1, 3, 3),
    (3, 1, 2),
    (5, 2, 1),
    (1, 4, 1);



SELECT
    o.id,
    o.styleId,
    o.metalId,
    o.sizeId,
    Styles.id AS style_id,
    Styles.style AS style,
    Styles.price AS style_price,
    Metals.id AS metal_id,
    Metals.metal AS metal,
    Metals.price AS metal_price,
    Sizes.id AS size_id,
    Sizes.carets AS carets,
    Sizes.price AS size_price
        FROM Orders o
        LEFT JOIN Styles ON o.styleId = Styles.id
        LEFT JOIN Metals ON o.metalId = Metals.id
        LEFT JOIN Sizes ON o.sizeId = Sizes.id
        GROUP BY o.id;

-- Simple Table with names and order price 
SELECT
    o.id,
    Styles.style AS style,
    Metals.metal AS metal,
    Sizes.carets AS carets,
    Sizes.price AS size_price
        FROM Orders o
        LEFT JOIN Styles ON o.styleId = Styles.id
        LEFT JOIN Metals ON o.metalId = Metals.id
        LEFT JOIN Sizes ON o.sizeId = Sizes.id
        GROUP BY o.id;

SELECT o.id, o.metalId, o.styleId, o.sizeId, FROM Orders o WHERE o.id = 24;