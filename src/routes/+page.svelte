<script lang="ts">
	import { uploadVideo } from '$lib/api/upload';

	let file = $state<FileList | null>(null);
	let visibility = $state<'public' | 'private'>('private');
	let title = $state('Untitled')
	let bio = $state('No Description')
	let keywords = $state('lame, boring')

	function handleUpload() {
		if ( file && file.length > 0) {
			console.log('Uploading file:', file[0]);
			uploadVideo(file[0])
				.then((response) => {
					console.log('Upload successful:', response);
				})
				.catch((error) => {
					console.error('Upload failed:', error);
				});
		}
	}

</script>

<svelte:head>
	<title>Auto Upload</title>
	<meta name="description" content="Upload a short-form video to multiple social platforms." />
</svelte:head>

<main class="min-h-screen bg-black px-4 py-12 text-white sm:px-6 lg:py-20">
	<div class="mx-auto max-w-xl">
		<header class="mb-8 text-center">
			<h1 class="text-4xl font-bold tracking-tight sm:text-5xl">Auto Upload</h1>
			<p class="mx-auto mt-4 max-w-md text-base leading-7 text-zinc-300">
				Upload all the short form slop in one place.
			</p>
		</header>

		<section class="rounded-2xl border border-zinc-700 bg-zinc-900 p-6 shadow-sm sm:p-5">
			<div>
				<!-- bind:files links the selected files to our variable -->
				<input
					type="file"
					id="file-input"
					accept="video/*"
					class="mt-4 block w-full cursor-pointer rounded-lg border border-zinc-600 bg-zinc-800 text-sm text-white file:mr-4 file:cursor-pointer file:border-0 file:bg-white file:px-4 file:py-2.5 file:font-semibold file:text-black hover:file:bg-zinc-200 focus:border-white focus:ring-white"
					bind:files={file}
				/>
			</div>

			<div class="flex flex-col items-center gap-4">
					<input type="text" id="title" name="title" class="mt-4 w-full rounded-lg border border-zinc-600 bg-zinc-800 p-3 text-white placeholder:text-zinc-400 focus:border-white focus:ring-white" placeholder="Video title" bind:value={title}>

					<textarea
							id="description"
							name="description"
							class="h-40 w-full rounded-lg border border-zinc-600 bg-zinc-800 p-3 text-white placeholder:text-zinc-400 focus:border-white focus:ring-2 focus:ring-white"
							placeholder="Description" bind:value={bio}></textarea>
					<input type="text" id="keywords" name="keywords" class="w-full rounded-lg border border-zinc-600 bg-zinc-800 p-3 text-white placeholder:text-zinc-400 focus:border-white focus:ring-white focus:border-white focus:ring-white" placeholder="Keywords (swag, bla bla) bind:value={keywords}">
				
			</div>
			<fieldset class="mt-6">
				<legend class="mb-2 font-medium">Visibility</legend>
				<div class="flex gap-6">
					<label class="flex items-center gap-2">
						<input type="checkbox" checked={visibility === 'private'} class="rounded border-zinc-500 bg-zinc-800 text-white focus:ring-white" onchange={(event) => { visibility = 'private'; event.currentTarget.checked = true; }} />
						Private
					</label>
					<label class="flex items-center gap-2">
						<input type="checkbox" checked={visibility === 'public'} class="rounded border-zinc-500 bg-zinc-800 text-white focus:ring-white" onchange={(event) => { visibility = 'public'; event.currentTarget.checked = true; }} />
						Public
					</label>
				</div>
			</fieldset>
			<button
				class="mt-8 w-full rounded-lg bg-white px-6 py-3 text-sm font-semibold text-black shadow-sm transition hover:bg-zinc-200 focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-black focus:outline-none"
				onclick={handleUpload}
			>
				Upload
			</button>
		</section>
	</div>
</main>
