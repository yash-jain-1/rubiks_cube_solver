import { Cube, moveConfig } from './cube';
import { getSolution } from './api';

const moveDisplay = document.getElementById('move-display')!;
const scrambleBtn = document.getElementById('scramble-btn') as HTMLButtonElement;
const solveBtn = document.getElementById('solve-btn') as HTMLButtonElement;
const moveControlsContainer = document.getElementById('move-controls')!;

let moveHistory: string[] = [];

function updateMoveDisplay() {
    moveDisplay.textContent = moveHistory.join(' ');
}

function setButtonsEnabled(enabled: boolean) {
    scrambleBtn.disabled = !enabled;
    solveBtn.disabled = !enabled;
    document.querySelectorAll('#move-controls button').forEach(btn => {
        (btn as HTMLButtonElement).disabled = !enabled;
    });
}

export function initUI(cube: Cube) {
    // --- Create Move Buttons ---
    Object.keys(moveConfig).forEach(move => {
        const button = document.createElement('button');
        button.textContent = move;
        button.addEventListener('click', () => {
            if (cube.getIsAnimating()) return;
            moveHistory.push(move);
            updateMoveDisplay();
            cube.performMove(move);
        });
        moveControlsContainer.appendChild(button);
    });

    // --- Main Control Listeners ---
    scrambleBtn.addEventListener('click', () => {
        if (cube.getIsAnimating()) return;
        moveHistory = [];
        updateMoveDisplay();
        const moves = Object.keys(moveConfig);
        for (let i = 0; i < 25; i++) {
            const randomMove = moves[Math.floor(Math.random() * moves.length)];
            cube.performMove(randomMove);
        }
    });

    solveBtn.addEventListener('click', async () => {
        if (cube.getIsAnimating()) return;
        
        setButtonsEnabled(false);
        moveDisplay.textContent = 'Reading cube state...';

        // Brief delay to allow UI to update before potentially heavy computation
        await new Promise(resolve => setTimeout(resolve, 50));
        
        const faceletString = cube.getFaceletString();
        if (faceletString.includes('?')) {
            moveDisplay.textContent = 'Error reading cube state. Please try again.';
            setButtonsEnabled(true);
            return;
        }

        moveDisplay.textContent = 'Connecting to solver...';

        try {
            const solution = await getSolution(faceletString);
            moveHistory = [];
            moveDisplay.textContent = `Solution found! Executing: ${solution}`;
            const solutionMoves = solution.trim().split(/\s+/);
            solutionMoves.forEach(move => cube.performMove(move));
        } catch (error) {
            moveDisplay.textContent = `Error: ${(error as Error).message}`;
        } finally {
            // Re-enable buttons after the animation starts/finishes
            const checkAnimation = setInterval(() => {
                if (!cube.getIsAnimating()) {
                    setButtonsEnabled(true);
                    clearInterval(checkAnimation);
                }
            }, 100);
        }
    });
}
