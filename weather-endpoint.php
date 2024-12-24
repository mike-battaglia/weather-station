<?php
/**
 * Plugin Name: Weather Data API
 * Description: Custom plugin to create a "Weather Data" CPT and receive weather data via REST API.
 * Version: 1.0
 * Author: Devon Ray Battaglia
 */

// Register Custom Post Type "Weather Data"
function create_weather_data_cpt() {
    $labels = array(
        'name' => _x('Weather Data', 'Post Type General Name', 'textdomain'),
        'singular_name' => _x('Weather Data', 'Post Type Singular Name', 'textdomain'),
        'menu_name' => __('Weather Data', 'textdomain'),
        'all_items' => __('All Weather Data', 'textdomain'),
        'add_new_item' => __('Add New Weather Data', 'textdomain'),
    );

    $args = array(
        'label' => __('Weather Data', 'textdomain'),
        'labels' => $labels,
        'supports' => array('title', 'editor', 'custom-fields'),
        'public' => true,
        'show_in_rest' => true,
        'has_archive' => true,
    );

    register_post_type('weather_data', $args);
}
add_action('init', 'create_weather_data_cpt');

// Register REST API Endpoint to receive weather data
function register_weather_data_endpoint() {
    register_rest_route('custom/v1', '/weather', array(
        'methods' => 'POST',
        'callback' => 'handle_weather_data',
        'permission_callback' => 'verify_api_key',
    ));
}
add_action('rest_api_init', 'register_weather_data_endpoint');

// Verify API key for authentication
function verify_api_key(WP_REST_Request $request) {
    $api_key = $request->get_header('X-API-Key');
    $valid_api_key = get_option('weather_data_api_key');

    if ($api_key && $api_key === $valid_api_key) {
        return true;
    }

    return new WP_Error('forbidden', 'Invalid API Key', array('status' => 403));
}

// Callback to handle incoming weather data
function handle_weather_data(WP_REST_Request $request) {
    $params = $request->get_json_params();

    // Sanitize and extract the data
    $timestamp = sanitize_text_field($params['timestamp'] ?? '');
    $temperature_f = floatval($params['temperature_f'] ?? 0);
    $humidity_percent = floatval($params['humidity_percent'] ?? 0);
    $pressure_inhg = floatval($params['pressure_inhg'] ?? 0);
    $dew_point_f = floatval($params['dew_point_f'] ?? 0);
    $feels_like_f = floatval($params['feels_like_f'] ?? 0);
    $wind_speed_mph = floatval($params['wind_speed_mph'] ?? 0);
    $wind_direction_degrees = intval($params['wind_direction_degrees'] ?? 0);
    $uv_index = intval($params['uv_index'] ?? 0);
    $cloud_cover_percent = intval($params['cloud_cover_percent'] ?? 0);
    $visibility_miles = floatval($params['visibility_miles'] ?? 0);

    // Create a new Weather Data post
    $post_id = wp_insert_post(array(
        'post_type' => 'weather_data',
        'post_title' => 'Weather Data - ' . $timestamp,
        'post_status' => 'publish',
        'meta_input' => array(
            'temperature_f' => $temperature_f,
            'humidity_percent' => $humidity_percent,
            'pressure_inhg' => $pressure_inhg,
            'dew_point_f' => $dew_point_f,
            'feels_like_f' => $feels_like_f,
            'wind_speed_mph' => $wind_speed_mph,
            'wind_direction_degrees' => $wind_direction_degrees,
            'uv_index' => $uv_index,
            'cloud_cover_percent' => $cloud_cover_percent,
            'visibility_miles' => $visibility_miles,
        ),
    ));

    if ($post_id) {
        return new WP_REST_Response(['status' => 'success', 'post_id' => $post_id], 200);
    } else {
        return new WP_REST_Response(['status' => 'error', 'message' => 'Failed to create post'], 500);
    }
}

// Display Weather Data on the Single Post Page
function display_weather_data_content($content) {
    if (is_singular('weather_data')) {
        global $post;
        $weather_data = get_post_meta($post->ID);

        $additional_content = '<h3>Weather Data Details (Imperial Units):</h3>';
        $additional_content .= '<p><strong>Temperature (F):</strong> ' . esc_html($weather_data['temperature_f'][0]) . '</p>';
        $additional_content .= '<p><strong>Humidity (%):</strong> ' . esc_html($weather_data['humidity_percent'][0]) . '</p>';
        $additional_content .= '<p><strong>Pressure (inHg):</strong> ' . esc_html($weather_data['pressure_inhg'][0]) . '</p>';
        $additional_content .= '<p><strong>Dew Point (F):</strong> ' . esc_html($weather_data['dew_point_f'][0]) . '</p>';
        $additional_content .= '<p><strong>Feels Like (F):</strong> ' . esc_html($weather_data['feels_like_f'][0]) . '</p>';
        $additional_content .= '<p><strong>Wind Speed (mph):</strong> ' . esc_html($weather_data['wind_speed_mph'][0]) . '</p>';
        $additional_content .= '<p><strong>Wind Direction (Degrees):</strong> ' . esc_html($weather_data['wind_direction_degrees'][0]) . '</p>';
        $additional_content .= '<p><strong>UV Index:</strong> ' . esc_html($weather_data['uv_index'][0]) . '</p>';
        $additional_content .= '<p><strong>Cloud Cover (%):</strong> ' . esc_html($weather_data['cloud_cover_percent'][0]) . '</p>';
        $additional_content .= '<p><strong>Visibility (Miles):</strong> ' . esc_html($weather_data['visibility_miles'][0]) . '</p>';

        $content .= $additional_content;
    }

    return $content;
}
add_filter('the_content', 'display_weather_data_content');

// Create an options page for API key
function weather_data_settings_menu() {
    add_options_page(
        'Weather Data API Settings',
        'Weather Data API',
        'manage_options',
        'weather-data-api',
        'weather_data_settings_page'
    );
}
add_action('admin_menu', 'weather_data_settings_menu');

// Render the settings page
function weather_data_settings_page() {
    ?>
    <div class="wrap">
        <h1>Weather Data API Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('weather_data_settings_group');
            do_settings_sections('weather-data-api');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}

// Register settings for the API key
function weather_data_settings_init() {
    register_setting('weather_data_settings_group', 'weather_data_api_key');

    add_settings_section(
        'weather_data_settings_section',
        'API Key Settings',
        null,
        'weather-data-api'
    );

    add_settings_field(
        'weather_data_api_key',
        'API Key',
        'weather_data_api_key_field_render',
        'weather-data-api',
        'weather_data_settings_section'
    );
}
add_action('admin_init', 'weather_data_settings_init');

// Render the API key field
function weather_data_api_key_field_render() {
    $api_key = get_option('weather_data_api_key');
    ?>
    <input type="text" name="weather_data_api_key" value="<?php echo esc_attr($api_key); ?>" size="50">
    <?php
}