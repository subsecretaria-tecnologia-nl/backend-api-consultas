@component('mail::layout')
{{-- Header --}}
@slot('header')
    @component('mail::header', ['url' => config('app.url')])
        <img src="data:image/png;base64,{{ base64_encode(file_get_contents(public_path('images/logo_tesoreria.png'))) }}" width="100px"><br>
       {{ config('app.name') }}
    @endcomponent
@endslot

{{-- Intro Lines --}}
@isset($data["introLines"])
@foreach ($data['introLines'] as $line)
{{ $line }}

@endforeach
@endisset
@isset($data["bodyText"])
{{ print($data["bodyText"]) }}
@endisset

@component('mail::button', ['url' => config('app.url'), 'color' => $data['color']])
Ir a Sitio
@endcomponent

{{-- Subcopy --}}
@isset($data['actionText'])
    @slot('subcopy')
        @component('mail::subcopy')
        @lang(
            "Si tiene problemas para hacer clic en el botón \":actionText\", copia y pega la siguiente URL \n".
            'en su navegador web: [:actionURL](:actionURL)',
            [
                'actionText' => $data['actionText'],
                'actionURL' => config('app.url'),
            ]
        )
        @endcomponent
    @endslot
@endisset
{{-- Footer --}}
@slot('footer')
    @component('mail::footer')
        © {{ date('Y') }} {{ config('app.name') }}. @lang('All rights reserved.')
    @endcomponent
@endslot
@endcomponent
