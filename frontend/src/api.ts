// IMPORTANT: Replace this with the actual URL of your Python backend solver.
const API_URL = 'http://127.0.0.1:5000/solve'; // Example for a local Flask server

/**
 * Sends the cube's state to the backend solver and returns the solution.
 * @param faceletString A 54-character string representing the cube's state.
 * @returns A promise that resolves to the solution string (e.g., "R U R' F'").
 */
export async function getSolution(faceletString: string): Promise<string> {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                state: faceletString,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ message: 'Server returned an error' }));
            throw new Error(errorData.message || `HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (!data.solution || typeof data.solution !== 'string') {
            throw new Error('Invalid solution format received from server.');
        }

        return data.solution;
    } catch (error) {
        console.error('Failed to fetch solution:', error);
        if (error instanceof TypeError) { // Network error
            throw new Error('Cannot connect to the solver. Is the backend running?');
        }
        throw error; // Re-throw other errors to be handled by the UI
    }
}
