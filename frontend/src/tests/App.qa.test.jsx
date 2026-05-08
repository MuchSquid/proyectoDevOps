import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import App from "../App";

describe("Uteblo QA UI coverage", () => {
  it("muestra la sección principal de Libros", () => {
  render(<App />);

  expect(screen.getAllByText(/libros/i).length).toBeGreaterThan(0);
});

  it("muestra el contador del catálogo de libros", () => {
    render(<App />);
    expect(screen.getByText(/libros en el catálogo/i)).toBeInTheDocument();
  });

  it("muestra el campo de búsqueda de libros", () => {
    render(<App />);
    expect(
      screen.getByPlaceholderText(/buscar por título o editorial/i)
    ).toBeInTheDocument();
  });

  it("permite escribir en el campo de búsqueda", () => {
    render(<App />);

    const searchInput = screen.getByPlaceholderText(
      /buscar por título o editorial/i
    );

    fireEvent.change(searchInput, { target: { value: "orwell" } });

    expect(searchInput).toHaveValue("orwell");
  });

  it("muestra el botón para agregar libro", () => {
    render(<App />);
    expect(screen.getByText(/agregar libro/i)).toBeInTheDocument();
  });

  it("muestra los módulos principales del sistema", () => {
    render(<App />);

    expect(screen.getAllByText(/libros/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/usuarios/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/préstamos/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/reservas/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/multas/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/notificaciones/i).length).toBeGreaterThan(0);
  });
});