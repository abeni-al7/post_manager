<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class PostIndexRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'page' => ['integer', 'min:1'],
            'per_page' => ['integer', 'min:1', 'max:100'],
            'category' => ['string', 'max:100'],
            'search' => ['string', 'max:255'],
            'sort' => ['string', 'in:title,published_date,created_at,author,word_count'],
            'direction' => ['string', 'in:asc,desc'],
        ];
    }
}