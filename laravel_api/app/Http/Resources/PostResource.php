<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class PostResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'subtitle' => $this->subtitle,
            'author' => $this->author,
            'content' => $this->when($request->routeIs('posts.show'), $this->content),
            'category' => $this->category,
            'source_file' => $this->source_file,
            'volume' => $this->volume,
            'issue_number' => $this->issue_number,
            'published_date' => $this->published_date?->format('Y-m-d'),
            'word_count' => $this->word_count,
            'images' => PostImageResource::collection($this->whenLoaded('images')),
            'created_at' => $this->created_at?->toISOString(),
            'updated_at' => $this->updated_at?->toISOString(),
        ];
    }
}