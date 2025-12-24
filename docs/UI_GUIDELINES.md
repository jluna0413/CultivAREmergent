# UI Guidelines

This document provides guidelines for the UI components and design patterns used in the CultivAR Flutter application.

## Colors

-   **Primary:** Green (e.g., `#4CAF50`)
-   **Accent:** A slightly lighter green (e.g., `#66BB6A`)
-   **Background:** Dark grey (e.g., `#1a1a1a`, `#2d2d2d`)
-   **Text:** White or light grey

## Typography

-   **Font:** Roboto (or system default)
-   **Headings:** Bold, larger font size
-   **Body:** Regular font size

## Core Widgets

### `CustomButton`

A custom button with primary and secondary styles.

-   **Primary:** `ElevatedButton` with a gradient background.
-   **Secondary:** `OutlinedButton`.

### `CustomTextField`

A custom text field with a consistent style.

-   Uses `TextFormField` with an `OutlineInputBorder`.

### `GlassCard`

A card with a frosted glass effect.

-   Uses `BackdropFilter` with a `blur` effect.

## Design Patterns

### State Management

-   **Riverpod:** Used for state management throughout the application.
-   **AsyncValue:** Used to handle loading and error states from asynchronous operations.

### Navigation

-   **GoRouter:** Used for declarative routing and deep linking.
-   **Authentication Guards:** Implemented using GoRouter's redirect functionality to protect routes.
