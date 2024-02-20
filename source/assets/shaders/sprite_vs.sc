$input a_position
$output v_texcoord0

#include <bgfx_shader.sh>

void main() {
	gl_Position = mul(u_modelViewProj, vec4(a_position, 1.0));
	v_texcoord0 = vec2(a_position.x+0.5,a_position.z+0.5);
}
