

$(document).ready( function () {
    $('.table').paging({limit:15});
    NProgress.start();
    NProgress.done();

    // $('#itemTable').DataTable();
} );