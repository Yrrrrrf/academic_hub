import { writable } from 'svelte/store';

export const api_url = writable('http://127.0.0.1:8000');

export const access_token = writable('');
export const some_other_value = writable('some_penchs');

export const user_type = writable('student');


export const current_table = writable('general_user');
export const current_tab = writable('all');

export const default_user = {
    email: 'user0@example.com',
    password: 'string'
}

