import { work_c } from './modul_c.js';

export function work_d(n) {
    if (n > 0) {
        console.log(`d: ${n}`);
        work_c(n - 1);
    }
}
