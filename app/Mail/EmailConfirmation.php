<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Mail\Mailables\Envelope;
use Illuminate\Queue\SerializesModels;

class EmailConfirmation extends Mailable
{
    use Queueable, SerializesModels;
    public $data;
    public $title;
    /**
     * Create a new message instance.
     */
    public function __construct($title,$data)
    {
        $this->data=$data;
        $this->title=$title;
    }

    /**
     * Get the message envelope.
     */
    public function envelope(): Envelope
    {
        return new Envelope(
            subject: 'Email Confirmation',
        );
    }

    /**
     * Get the message content definition.
     */
    public function build()
    {
        return $this->markdown('Mail.userMail')->subject($this->title);
    }
}
