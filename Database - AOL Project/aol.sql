-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 29, 2024 at 12:12 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aol`
--

-- --------------------------------------------------------

--
-- Table structure for table `carpart`
--

CREATE TABLE `carpart` (
  `PartID` varchar(10) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `carpart`
--

INSERT INTO `carpart` (`PartID`, `Name`, `Description`, `Price`) VALUES
('P001', 'Engine Oil', 'Synthetic Oil', 100.00),
('P002', 'Brake Pad', 'Disc Brake Pad', 200.00),
('P003', 'Air Filter', 'High-Quality Air', 150.00),
('P004', 'Spark Plug', 'High-Performance', 80.00),
('P005', 'Battery', 'Maintenance-Free', 300.00);

-- --------------------------------------------------------

--
-- Table structure for table `orderdetails`
--

CREATE TABLE `orderdetails` (
  `DetailID` varchar(10) NOT NULL,
  `OrderID` varchar(10) DEFAULT NULL,
  `PartID` varchar(10) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderdetails`
--

INSERT INTO `orderdetails` (`DetailID`, `OrderID`, `PartID`, `Quantity`) VALUES
('D001', 'OR001', 'P001', 50),
('D002', 'OR002', 'P002', 20),
('D003', 'OR003', 'P001', 30),
('D004', 'OR004', 'P003', 10),
('D005', 'OR005', 'P002', 25);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `OrderID` varchar(10) NOT NULL,
  `OrderDate` date DEFAULT NULL,
  `SupplierID` varchar(10) DEFAULT NULL,
  `WarehouseID` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`OrderID`, `OrderDate`, `SupplierID`, `WarehouseID`) VALUES
('OR001', '2024-01-01', 'S001', 'W001'),
('OR002', '2024-03-12', 'S002', 'W001'),
('OR003', '2024-12-17', 'S001', 'W002'),
('OR004', '2024-05-12', 'S003', 'W003'),
('OR005', '2024-10-10', 'S002', 'W002');

-- --------------------------------------------------------

--
-- Table structure for table `supplier`
--

CREATE TABLE `supplier` (
  `SupplierID` varchar(10) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Contact` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supplier`
--

INSERT INTO `supplier` (`SupplierID`, `Name`, `Contact`) VALUES
('S001', 'Alpha', '123456'),
('S002', 'Beta', '654321'),
('S003', 'Charlie', '456321'),
('S004', 'Delta', '789456'),
('S005', 'Eco', '147852');

-- --------------------------------------------------------

--
-- Table structure for table `warehouse`
--

CREATE TABLE `warehouse` (
  `WarehouseID` varchar(10) NOT NULL,
  `Location` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `warehouse`
--

INSERT INTO `warehouse` (`WarehouseID`, `Location`) VALUES
('W001', 'Jakarta'),
('W002', 'Bandung'),
('W003', 'Surabaya'),
('W004', 'Yogyakarta'),
('W005', 'Medan');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `carpart`
--
ALTER TABLE `carpart`
  ADD PRIMARY KEY (`PartID`);

--
-- Indexes for table `orderdetails`
--
ALTER TABLE `orderdetails`
  ADD PRIMARY KEY (`DetailID`),
  ADD KEY `OrderID` (`OrderID`),
  ADD KEY `PartID` (`PartID`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `SupplierID` (`SupplierID`),
  ADD KEY `WarehouseID` (`WarehouseID`);

--
-- Indexes for table `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`SupplierID`);

--
-- Indexes for table `warehouse`
--
ALTER TABLE `warehouse`
  ADD PRIMARY KEY (`WarehouseID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orderdetails`
--
ALTER TABLE `orderdetails`
  ADD CONSTRAINT `orderdetails_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `orders` (`OrderID`),
  ADD CONSTRAINT `orderdetails_ibfk_2` FOREIGN KEY (`PartID`) REFERENCES `carpart` (`PartID`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`SupplierID`) REFERENCES `supplier` (`SupplierID`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`WarehouseID`) REFERENCES `warehouse` (`WarehouseID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
