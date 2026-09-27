<script lang="ts">
	import { uploadVideo } from '$lib/api/upload';

	let file = $state<FileList | null>(null);

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

<main class="min-h-screen bg-slate-50 px-4 py-12 text-slate-900 sm:px-6 lg:py-20">
	<div class="mx-auto max-w-xl">
		<header class="mb-8 text-center">
			<h1 class="text-4xl font-bold tracking-tight sm:text-5xl">Auto Upload</h1>
			<p class="mx-auto mt-4 max-w-md text-base leading-7 text-slate-600">
				Upload all the short form slop in one place.
			</p>
		</header>

		<section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-5">
			<div>
				<!-- bind:files links the selected files to our variable -->
				<input
					type="file"
					id="file-input"
					accept="video/*"
					class="mt-4 block w-full cursor-pointer rounded-lg border border-slate-300 bg-slate-50 text-sm text-slate-600 file:mr-4 file:cursor-pointer file:border-0 file:bg-violet-50 file:px-4 file:py-2.5 file:font-semibold file:text-violet-700 hover:file:bg-violet-100 focus:border-violet-500 focus:ring-violet-500"
					bind:files={file}
				/>
			</div>
			<button
				class="mt-8 w-full rounded-lg bg-violet-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700 focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 focus:outline-none"
				onclick={handleUpload}
			>
				Upload
			</button>
		</section>
	</div>
</main>
