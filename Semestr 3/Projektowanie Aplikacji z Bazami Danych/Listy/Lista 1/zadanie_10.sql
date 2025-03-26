-- Usuwanie tabel dla zadania, żeby pokazać, że program działa
DROP TABLE IF EXISTS M1
DROP TABLE IF EXISTS S1
DROP TABLE IF EXISTS M2
DROP TABLE IF EXISTS S2
GO

-- Tworzenie tabeli M1
CREATE TABLE M1 (
    K INT NOT NULL PRIMARY KEY, -- Nie trzeba stosować NOT NULL w tym przypadku, ale zwiększa to czytelność kodu
    V VARCHAR(20),
);

-- Tworzenie tabeli S1
CREATE TABLE S1 (
    K INT NOT NULL PRIMARY KEY, -- Nie trzeba stosować NOT NULL w tym przypadku, ale zwiększa to czytelność kodu
    MFK INT, 
    V VARCHAR(20),
    CONSTRAINT FK_S1_M1 FOREIGN KEY (MFK) REFERENCES M1(K)
);

-- Tworzenie tabeli M2
CREATE TABLE M2 (
    K1 INT NOT NULL,
    K2 INT NOT NULL,
    V VARCHAR(20),
    PRIMARY KEY (K1, K2)
);

-- Tworzenie tabeli S2
CREATE TABLE S2 (
    K INT NOT NULL PRIMARY KEY,
    MFK1 INT,
    MFK2 INT,
    V VARCHAR(20),
    CONSTRAINT FK_S2_M2 FOREIGN KEY (MFK1, MFK2) REFERENCES M2(K1, K2)
);
GO

-- Dodanie danych testowych do tabeli M1
INSERT INTO M1 (K, V) VALUES (1, 'Value1'), (2, 'Value2'), (3, 'Value3');

-- Dodanie danych testowych do tabeli S1 (klucz obcy do M1)
INSERT INTO S1 (K, MFK, V) VALUES (1, 1, 'S1_Value1'), (2, 2, 'S1_Value2'), (3, 3, 'S1_Value3');

-- Dodanie danych testowych do tabeli M2
INSERT INTO M2 (K1, K2, V) VALUES (1, 1, 'M2_Value1'), (2, 2, 'M2_Value2');

-- Dodanie danych testowych do tabeli S2 (klucz obcy do M2)
INSERT INTO S2 (K, MFK1, MFK2, V) VALUES (1, 1, 1, 'S2_Value1'), (2, 2, 2, 'S2_Value2');
GO

-- Próba dodania rekordu z nieistniejącym kluczem obcym do tabeli S1
INSERT INTO S1 (K, MFK, V) VALUES (3, 5, 'Invalid');  -- To spowoduje błąd

-- Próba dodania rekordu z nieistniejącym kluczem obcym do tabeli S2
INSERT INTO S2 (K, MFK1, MFK2, V) VALUES (3, 3, 3, 'Invalid');  -- To spowoduje błąd
GO

-- Usunięcie kluczy obcych, aby je zmodyfikować
ALTER TABLE S1 DROP CONSTRAINT FK_S1_M1;
ALTER TABLE S2 DROP CONSTRAINT FK_S2_M2;

-- Dodanie klucza obcego z ON DELETE i ON UPDATE do S1
ALTER TABLE S1
ADD CONSTRAINT FK_S1_M1 FOREIGN KEY (MFK) REFERENCES M1(K)
ON DELETE CASCADE ON UPDATE NO ACTION;

-- Dodanie klucza obcego z ON DELETE i ON UPDATE do S2
ALTER TABLE S2
ADD CONSTRAINT FK_S2_M2 FOREIGN KEY (MFK1, MFK2) REFERENCES M2(K1, K2)
ON DELETE SET NULL ON UPDATE CASCADE;

-- Usunięcie rekordu z tabeli M1
DELETE FROM M1 WHERE K = 1;

-- Sprawdzenie, czy odpowiedni rekord w tabeli S1 również został usunięty
SELECT * FROM S1;

-- Usunięcie rekordu z tabeli M2
DELETE FROM M2 WHERE K1 = 1 AND K2 = 1;

-- Sprawdzenie, czy odpowiednie wartości w tabeli S2 zostały ustawione na NULL
SELECT * FROM S2;

-- Zmiana wartości klucza w tabeli M2
UPDATE M2 SET K1 = 3 WHERE K1 = 2 AND K2 = 2;

-- Sprawdzenie, czy klucz w tabeli S2 również został zaktualizowany
SELECT * FROM S2;

-- Sprawdzenie, 
SELECT * FROM M1;

SELECT * FROM M2;
GO

-- Usuwanie tabel na koniec programu
DROP TABLE M1;
DROP TABLE M2;
DROP TABLE S1;
DROP TABLE S2;
GO
