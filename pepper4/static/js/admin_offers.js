document.getElementById('selectAllOffers').addEventListener('change', function() {
    const checked = this.checked;
    document.querySelectorAll('.offer-checkbox').forEach(cb => cb.checked = checked);
    toggleScheduleBtn();
  });
  document.querySelectorAll('.offer-checkbox').forEach(cb => {
    cb.addEventListener('change', toggleScheduleBtn);
  });
  function toggleScheduleBtn() {
    const anyChecked = Array.from(document.querySelectorAll('.offer-checkbox')).some(cb => cb.checked);
    document.getElementById('scheduleRedirectBtn').disabled = !anyChecked;
  }
  
  document.getElementById('scheduleRedirectBtn').addEventListener('click', function() {
    var modal = new bootstrap.Modal(document.getElementById('redirectModal'));
    modal.show();
  });
  
  document.getElementById('redirectScheduleForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const offerIds = Array.from(document.querySelectorAll('.offer-checkbox:checked')).map(cb => cb.value);
    const redirectUrl = document.getElementById('redirectUrl').value;
    const activeFrom = document.getElementById('activeFrom').value;
    const activeTo = document.getElementById('activeTo').value;
    fetch('/admin/schedule_offer_redirects', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        offer_ids: offerIds,
        redirect_url: redirectUrl,
        active_from: activeFrom,
        active_to: activeTo
      })
    }).then(resp => resp.json()).then(data => {
      if (data.success) {
        alert('Redirect scheduled!');
        location.reload();
      } else {
        alert('Error scheduling redirect.');
      }
    });
  });


// // Wait for DOM to be ready
// document.addEventListener('DOMContentLoaded', function() {
//     const selectAll = document.getElementById('selectAllOffers');
//     const checkboxes = document.querySelectorAll('.offer-checkbox');
//     const applyBtn = document.getElementById('applyBulkBtn');
//     const urlInput = document.getElementById('bulkUrl');
//     const fromInput = document.getElementById('bulkFrom');
//     const toInput = document.getElementById('bulkTo');
  
//     function updateApplyBtnState() {
//       // Enable if at least one offer is checked and all inputs are filled
//       const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
//       const allInputsFilled = urlInput.value && fromInput.value && toInput.value;
//       applyBtn.disabled = !(anyChecked && allInputsFilled);
//     }
  
//     // Select All logic
//     selectAll.addEventListener('change', function() {
//       checkboxes.forEach(cb => cb.checked = selectAll.checked);
//       updateApplyBtnState();
//     });
  
//     // Individual checkbox logic
//     checkboxes.forEach(cb => {
//       cb.addEventListener('change', function() {
//         // If any unchecked, uncheck selectAll; if all checked, check selectAll
//         selectAll.checked = Array.from(checkboxes).every(cb => cb.checked);
//         updateApplyBtnState();
//       });
//     });
  
//     // Input fields logic
//     [urlInput, fromInput, toInput].forEach(input => {
//       input.addEventListener('input', updateApplyBtnState);
//     });
  
//     // Initial state
//     updateApplyBtnState();
  
//     // (Functionality for submit can be added here, but you said to focus on UI for now)
//   });