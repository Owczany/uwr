// ! EXCLUDE
type T0 = Exclude<"a" | "b" | "c", "a">;
// * type T0 = "b" | "c";

type T1 = Exclude<"a" | "b" | "c", "a" | "b">;
// * type T1 = "c";

type T2 = Exclude<string | number | (() => void), Function>;
// * type T2 = string | number;

type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "square"; x: number }
    | { kind: "triangle"; x: number; y: number };

type T3 = Exclude<Shape, { kind: "circle" }>
// * type T3 = {
// *     kind: "square";
// *     x: number;
// * } | {
// *     kind: "triangle";
// *     x: number;
// *     y: number;
// * }

// ! EXTRACT
type T4 = Extract<"a" | "b" | "c", "a" | "f">;
// * type T4 = "a";

type T5 = Extract<string | number | (() => void), Function>;
// * type T5 = () => void;
 
type T6 = Extract<Shape, { kind: "circle" }>
// * type T6 = {
// *    kind: "circle";
// *    radius: number;
// * }


// ! PICK
interface Todo {
    title: string;
    description: string;
    completed: boolean;
}

type TodoPreview = Pick<Todo, "title" | "completed">;

const todo: TodoPreview = {
    title: "Clean room",
    completed: false,
};

// ! OMIT
type TodoInfo = Omit<Todo, "completed" | "createdAt">;
 
const todoInfo: TodoInfo = {
  title: "Pick up kids",
  description: "Kindergarten closes at 5pm",
};

// ! RECORD
type Roles = 'admin' | 'user' | 'guest';
type Permissions2 = Record<Roles, boolean>;

const permissions: Permissions2 = {
    admin: true,
    user: false,
    guest: false,
};

// ! REQUIRED
type User = {
    name?: string;
    age?: number;
};

type FullUser = Required<User>;

const user: FullUser = {
    name: 'Alice',
    age: 25,
};

// ! READONLY
type ImmutableUser = Readonly<User>;

const readOnlyUser: ImmutableUser = {
    name: 'Alice',
    age: 25,
};

// readOnlyUser.name = 'Bob'; // Błąd kompilacji: właściwość tylko do odczytu

// ! PARTIAL
type PartialUser = Partial<User>;

const partialUser: PartialUser = {
    name: 'Alice', // Właściwość `age` jest opcjonalna
};