/**
 * Synthetic Data for Biblioteca Reservas
 * This file defines the data schema and mock records for Books, Users, and Reservations.
 * Use this as a reference for backend API implementation.
 */

export const MOCK_BOOKS = [
  {
    id: '1',
    title: 'The Art of Automation',
    author: 'Alex Rivera',
    genre: 'Technology',
    year: 2023,
    availability: 'available',
    description: 'A comprehensive guide to modern workflow automation and agentic AI.',
    cover: 'https://images.unsplash.com/photo-1589998059171-988d887df646?auto=format&fit=crop&q=80&w=400',
  },
  {
    id: '2',
    title: 'Cinematic Interfaces',
    author: 'Elena Glass',
    genre: 'Design',
    year: 2024,
    availability: 'reserved',
    description: 'Exploring the intersection of film aesthetics and user interface design.',
    cover: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=400',
  },
  {
    id: '3',
    title: 'FastAPI Mastery',
    author: 'Lucas Backend',
    genre: 'Programming',
    year: 2022,
    availability: 'available',
    description: 'Build high-performance APIs with Python and modern async patterns.',
    cover: 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&q=80&w=400',
  },
  {
    id: '4',
    title: 'Testing for QA Engineers',
    author: 'Sarah Quality',
    genre: 'Quality Assurance',
    year: 2023,
    availability: 'available',
    description: 'Advanced strategies for automated testing in modern web applications.',
    cover: 'https://images.unsplash.com/photo-1509021436665-8f07dbf5bf1d?auto=format&fit=crop&q=80&w=400',
  },
  {
    id: '5',
    title: 'The Monorepo Handbook',
    author: 'Jordan Ops',
    genre: 'Architecture',
    year: 2024,
    availability: 'maintenance',
    description: 'Mastering large-scale codebase management with modern tooling.',
    cover: 'https://images.unsplash.com/photo-1532012197367-6a56a21ef44d?auto=format&fit=crop&q=80&w=400',
  },
];

export const MOCK_USERS = [
  {
    id: 'u1',
    name: 'Esteban User',
    role: 'admin',
    email: 'esteban@example.com',
  },
  {
    id: 'u2',
    name: 'Jane Doe',
    role: 'member',
    email: 'jane@example.com',
  },
];

export const MOCK_RESERVATIONS = [
  {
    id: 'r1',
    bookId: '2',
    userId: 'u2',
    startDate: '2026-05-01',
    endDate: '2026-05-15',
    status: 'active',
  },
];
