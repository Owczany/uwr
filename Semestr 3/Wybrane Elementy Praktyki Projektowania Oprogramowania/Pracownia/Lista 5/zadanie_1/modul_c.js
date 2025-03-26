import { work_d } from './modul_d.js';

export function work_c(n) {
    if (n > 0) {
        console.log(`c: ${n}`);
        work_d(n - 1);
    }
}
