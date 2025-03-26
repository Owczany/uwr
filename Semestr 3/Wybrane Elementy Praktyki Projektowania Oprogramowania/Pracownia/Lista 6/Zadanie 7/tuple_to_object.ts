type TupleToObject<T extends readonly (keyof any)[]> = {
    [Key in T[number]]: T
}
