import * as THREE from 'three';
import * as TWEEN from '@tweenjs/tween.js';

const CUBELET_SIZE = 1;
const SPACING = 0.05;

// --- TYPE DEFINITIONS ---
interface Move {
    axis: 'x' | 'y' | 'z';
    layer: number;
    direction: 1 | -1;
}

export const moveConfig: { [key: string]: Move } = {
    'U': { axis: 'y', layer: 1, direction: -1 }, 'U\'': { axis: 'y', layer: 1, direction: 1 },
    'D': { axis: 'y', layer: -1, direction: 1 }, 'D\'': { axis: 'y', layer: -1, direction: -1 },
    'L': { axis: 'x', layer: -1, direction: 1 }, 'L\'': { axis: 'x', layer: -1, direction: -1 },
    'R': { axis: 'x', layer: 1, direction: -1 }, 'R\'': { axis: 'x', layer: 1, direction: 1 },
    'F': { axis: 'z', layer: 1, direction: -1 }, 'F\'': { axis: 'z', layer: 1, direction: 1 },
    'B': { axis: 'z', layer: -1, direction: 1 }, 'B\'': { axis: 'z', layer: -1, direction: -1 },
};

export class Cube {
    private scene: THREE.Scene;
    private cubelets: THREE.Mesh[] = [];
    private isAnimating = false;
    private moveQueue: string[] = [];
    private materials: { [key: string]: THREE.MeshLambertMaterial };
    private colorToFaceMap: { [key: string]: string };

    constructor(scene: THREE.Scene) {
        this.scene = scene;
        this.materials = {
            'U': new THREE.MeshLambertMaterial({ color: 0xffffff }), // White
            'D': new THREE.MeshLambertMaterial({ color: 0xffff00 }), // Yellow
            'F': new THREE.MeshLambertMaterial({ color: 0x0000ff }), // Blue
            'B': new THREE.MeshLambertMaterial({ color: 0x00ff00 }), // Green
            'R': new THREE.MeshLambertMaterial({ color: 0xff0000 }), // Red
            'L': new THREE.MeshLambertMaterial({ color: 0xffa500 }), // Orange
            'black': new THREE.MeshLambertMaterial({ color: 0x1a1a1a }),
        };
        this.colorToFaceMap = {
            'ffffff': 'U', 'ffff00': 'D', '0000ff': 'F',
            '00ff00': 'B', 'ff0000': 'R', 'ffa500': 'L'
        };
        this.createCube();
    }

    private createCube() {
        for (let x = -1; x <= 1; x++) {
            for (let y = -1; y <= 1; y++) {
                for (let z = -1; z <= 1; z++) {
                    if (x === 0 && y === 0 && z === 0) continue;

                    const geometry = new THREE.BoxGeometry(CUBELET_SIZE - SPACING, CUBELET_SIZE - SPACING, CUBELET_SIZE - SPACING);
                    const faceMaterials = [
                        x === 1 ? this.materials.R : this.materials.black,
                        x === -1 ? this.materials.L : this.materials.black,
                        y === 1 ? this.materials.U : this.materials.black,
                        y === -1 ? this.materials.D : this.materials.black,
                        z === 1 ? this.materials.F : this.materials.black,
                        z === -1 ? this.materials.B : this.materials.black,
                    ];

                    const cubelet = new THREE.Mesh(geometry, faceMaterials);
                    cubelet.position.set(x * CUBELET_SIZE, y * CUBELET_SIZE, z * CUBELET_SIZE);
                    this.cubelets.push(cubelet);
                    this.scene.add(cubelet);
                }
            }
        }
    }

    public performMove(move: string) {
        if (!moveConfig[move]) return;
        this.moveQueue.push(move);
        if (!this.isAnimating) {
            this.processQueue();
        }
    }
    
    public getIsAnimating(): boolean {
        return this.isAnimating;
    }

    private processQueue() {
        if (this.moveQueue.length === 0) return;
        const move = this.moveQueue.shift()!;
        const { axis, layer, direction } = moveConfig[move];
        this.rotateFace(axis, layer, direction);
    }

    private rotateFace(axis: 'x' | 'y' | 'z', layer: number, direction: 1 | -1) {
        this.isAnimating = true;
        
        const pivot = new THREE.Group();
        this.scene.add(pivot);

        const cubeletsToRotate = this.cubelets.filter(c => Math.abs(c.position[axis] - layer) < 0.1);
        cubeletsToRotate.forEach(c => pivot.attach(c));

        const targetRotation = { val: Math.PI / 2 * direction };
        new TWEEN.Tween({ val: 0 })
            .to(targetRotation, 400)
            .easing(TWEEN.Easing.Quadratic.Out)
            .onUpdate((obj) => { pivot.rotation[axis] = obj.val; })
            .onComplete(() => {
                pivot.rotation[axis] = targetRotation.val;
                cubeletsToRotate.forEach(c => {
                    this.scene.attach(c);
                    c.position.round();
                    c.rotation.toVector3().round();
                });
                this.scene.remove(pivot);
                this.isAnimating = false;
                this.processQueue();
            })
            .start();
    }
    
    public getFaceletString(): string {
        const faceletString: string[] = [];
        const raycaster = new THREE.Raycaster();

        const facesToScan = {
            'U': { axis: 'y', dir: -1, order: (x: number, z: number) => ({ x, y: 1, z }) },
            'R': { axis: 'x', dir: -1, order: (y: number, z: number) => ({ x: 1, y: -y, z: -z }) },
            'F': { axis: 'z', dir: -1, order: (x: number, y: number) => ({ x, y: -y, z: 1 }) },
            'D': { axis: 'y', dir: 1, order: (x: number, z: number) => ({ x, y: -1, z: -z }) },
            'L': { axis: 'x', dir: 1, order: (y: number, z: number) => ({ x: -1, y: -y, z }) },
            'B': { axis: 'z', dir: 1, order: (x: number, y: number) => ({ x: -x, y: -y, z: -1 }) },
        };

        for (const faceKey in facesToScan) {
            const face = facesToScan[faceKey as keyof typeof facesToScan];
            for (let row = -1; row <= 1; row++) {
                for (let col = -1; col <= 1; col++) {
                    const pos = face.order(col, row);
                    const origin = new THREE.Vector3(pos.x * 2, pos.y * 2, pos.z * 2);
                    const direction = new THREE.Vector3();
                    direction[face.axis] = face.dir;
                    
                    raycaster.set(origin, direction);
                    const intersects = raycaster.intersectObjects(this.cubelets);

                    if (intersects.length > 0) {
                        const material = (intersects[0].object as THREE.Mesh).material as THREE.Material[];
                        const colorHex = (material[intersects[0].face!.materialIndex!] as THREE.MeshLambertMaterial).color.getHexString();
                        faceletString.push(this.colorToFaceMap[colorHex] || '?');
                    } else {
                        faceletString.push('?');
                    }
                }
            }
        }
        return faceletString.join('');
    }
}
