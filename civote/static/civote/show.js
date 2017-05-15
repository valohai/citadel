function showEntry(contestant, entryId) {
  document.getElementById('contestant').innerHTML = contestant.replace(/</g, '&lt;');
  document.getElementById('show-iframe').src = location.pathname + '?entry=' + entryId;
}
